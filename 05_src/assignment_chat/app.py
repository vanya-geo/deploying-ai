import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from typing import Optional
import os

from langchain.chat_models import init_chat_model

#bring in the graph for the assignment chat
from assignment_chat.main import get_graph

from utils.logger import get_logger

_logs = get_logger(__name__)


load_dotenv('.secrets')

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Missing OPENAI_API_KEY environment variable")
if not os.getenv("TAVILY_API_KEY"):
    raise RuntimeError("Missing TAVILY_API_KEY. Put it in .env or .secrets.")



llm = init_chat_model("gpt-4o-mini", model_provider="openai")
graph = get_graph() 

def assignment_chat(message: str, history: list[dict]) -> str:
    langchain_messages = []
    n = 0
    _logs.debug(f"History: {history}")
    for msg in history:
        if msg['role'] == 'user':
            langchain_messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            langchain_messages.append(AIMessage(content=msg['content']))
            n += 1
    langchain_messages.append(HumanMessage(content=message))

    state = {
        "messages": langchain_messages,
        "llm_calls": n
    }

    #response = llm.invoke(state) #this was breaking

    #instead of llm call, call the graph
    out_state = graph.invoke({"messages": langchain_messages})
    # LangGraph returns MessagesState: {"messages": [...]} (includes tool + AI messages, etc.)
    final_msg = out_state["messages"][-1]

    return getattr(final_msg, "content", str(final_msg))

chat = gr.ChatInterface(
    fn=assignment_chat,
    type="messages"
)

if __name__ == "__main__":
    _logs.info('Starting Assignment Chat App...')
    chat.launch()
