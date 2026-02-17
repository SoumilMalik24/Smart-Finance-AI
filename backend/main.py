import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
    AIMessageChunk
)

from mcp_client import client
from session_memory import (
    get_session_history,
    append_to_session
)

tools_cache = []
named_tools_cache = {}


@asynccontextmanager
async def lifespan(app):
    """Load MCP tools on startup."""
    global tools_cache, named_tools_cache

    tools_cache = await client.get_tools()
    named_tools_cache = {tool.name: tool for tool in tools_cache}
    yield


app = FastAPI(title="Financial Orchestrator AI", lifespan=lifespan)

# CORS: allow frontend origin (set FRONTEND_URL in Render env vars)
allowed_origins = ["http://localhost:5173", "http://localhost:3000"]
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


async def event_generator(session_id: str, user_input: str):
    MAX_TOOL_ROUNDS = 5  # Safety limit to prevent infinite loops

    try:
        # 1️⃣ Add user message to session
        user_msg = HumanMessage(content=user_input)
        append_to_session(session_id, user_msg)

        # 2️⃣ Setup LLM
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            streaming=True
        )

        if tools_cache:
            llm = llm.bind_tools(tools_cache)

        # 3️⃣ Agent Loop — keep going until GPT-4o stops calling tools
        for round_num in range(MAX_TOOL_ROUNDS):

            history = get_session_history(session_id)
            accumulated = AIMessageChunk(content="")

            # Stream LLM response
            async for chunk in llm.astream(history):
                accumulated += chunk
                if chunk.content:
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk.content})}\n\n"

            # Save AI message to session
            ai_message = AIMessage(
                content=accumulated.content,
                tool_calls=accumulated.tool_calls
            )
            append_to_session(session_id, ai_message)

            # If no tool calls, we're done
            if not accumulated.tool_calls:
                break

            # 4️⃣ Execute tool calls
            yield f"data: {json.dumps({'type': 'status', 'content': 'Using financial tools...'})}\n\n"

            for tc in accumulated.tool_calls:
                tool_name = tc["name"]
                tool_args = tc.get("args", {})
                tool_id = tc["id"]

                yield f"data: {json.dumps({'type': 'tool_start', 'tool': tool_name})}\n\n"

                tool_output = None
                tool_output_parsed = None
                try:
                    if tool_name in named_tools_cache:
                        tool_output = await named_tools_cache[tool_name].ainvoke(tool_args)

                        # MCP tools return a list of content blocks:
                        # [{"type": "text", "text": '{"image_base64": "..."}'}]
                        # We need to extract the text and parse it.
                        raw_text = None
                        if isinstance(tool_output, list) and len(tool_output) > 0:
                            first = tool_output[0]
                            if isinstance(first, dict) and "text" in first:
                                raw_text = first["text"]
                            elif isinstance(first, str):
                                raw_text = first
                        elif isinstance(tool_output, dict):
                            raw_text = json.dumps(tool_output)
                        elif isinstance(tool_output, str):
                            raw_text = tool_output

                        # Try to parse as JSON dict
                        if raw_text:
                            tool_result_content = raw_text
                            try:
                                tool_output_parsed = json.loads(raw_text)
                            except (json.JSONDecodeError, TypeError):
                                tool_output_parsed = None
                        else:
                            tool_result_content = str(tool_output)
                    else:
                        tool_result_content = json.dumps({"error": "Tool not found"})
                except Exception as e:
                    tool_result_content = json.dumps({"error": str(e)})

                # If the tool returned a chart image, send it as a
                # dedicated 'chart' event so the frontend renders it as
                # an <img> immediately — NOT as streaming text tokens.
                if isinstance(tool_output_parsed, dict) and "image_base64" in tool_output_parsed:
                    b64 = tool_output_parsed["image_base64"]
                    yield f"data: {json.dumps({'type': 'chart', 'src': f'data:image/png;base64,{b64}'})}\n\n"
                    # Tell GPT-4o the chart is already displayed.
                    tool_result_content = json.dumps({
                        "status": "success",
                        "note": "Chart image has already been rendered and displayed to the user inline. Do NOT output any base64 data, markdown image links, or image URLs. Simply refer to the chart as 'the chart above' or 'the chart shown'."
                    })

                tool_msg = ToolMessage(
                    tool_call_id=tool_id,
                    content=tool_result_content
                )
                append_to_session(session_id, tool_msg)

                yield f"data: {json.dumps({'type': 'tool_end', 'tool': tool_name})}\n\n"

            # Loop continues — GPT-4o will see tool results and may call more tools

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"


@app.post("/chat")
async def chat(request: ChatRequest):
    return StreamingResponse(
        event_generator(request.session_id, request.message),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
