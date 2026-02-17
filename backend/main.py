import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
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


class ChatRequest(BaseModel):
    session_id: str
    message: str


async def event_generator(session_id: str, user_input: str):

    try:
        # 1️⃣ Add user message to session
        user_msg = HumanMessage(content=user_input)
        append_to_session(session_id, user_msg)

        # Load updated history (includes system prompt + all messages)
        history = get_session_history(session_id)

        # 2️⃣ Setup LLM
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            streaming=True
        )

        if tools_cache:
            llm = llm.bind_tools(tools_cache)

        accumulated = AIMessageChunk(content="")

        # 3️⃣ First Pass — stream LLM response
        async for chunk in llm.astream(history):
            accumulated += chunk

            if chunk.content:
                yield f"data: {json.dumps({'type': 'token', 'content': chunk.content})}\n\n"

        # Convert to full AIMessage
        first_ai_message = AIMessage(
            content=accumulated.content,
            tool_calls=accumulated.tool_calls
        )

        append_to_session(session_id, first_ai_message)

        # 4️⃣ Handle Tool Calls
        if accumulated.tool_calls:

            yield f"data: {json.dumps({'type': 'status', 'content': 'Using financial tools...'})}\n\n"

            for tc in accumulated.tool_calls:

                tool_name = tc["name"]
                tool_args = tc.get("args", {})
                tool_id = tc["id"]

                yield f"data: {json.dumps({'type': 'tool_start', 'tool': tool_name})}\n\n"

                try:
                    if tool_name in named_tools_cache:
                        tool_output = await named_tools_cache[tool_name].ainvoke(tool_args)
                        tool_result_content = json.dumps(tool_output)
                    else:
                        tool_result_content = json.dumps({"error": "Tool not found"})

                except Exception as e:
                    tool_result_content = json.dumps({"error": str(e)})

                tool_msg = ToolMessage(
                    tool_call_id=tool_id,
                    content=tool_result_content
                )

                append_to_session(session_id, tool_msg)

                yield f"data: {json.dumps({'type': 'tool_end', 'tool': tool_name})}\n\n"

            # 5️⃣ Final Pass — stream response after tool results
            updated_history = get_session_history(session_id)

            final_accumulated = AIMessageChunk(content="")

            async for chunk in llm.astream(updated_history):
                final_accumulated += chunk

                if chunk.content:
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk.content})}\n\n"

            final_message = AIMessage(content=final_accumulated.content)
            append_to_session(session_id, final_message)

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
