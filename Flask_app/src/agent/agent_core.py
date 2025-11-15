from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import datetime

from .llm_engine import get_llm
from ..tools import get_all_tools
from ..utils.main_functions import load_prompt

# Create a single instance of the checkpointer to maintain state across requests
memory_checkpointer = MemorySaver()


def get_chat_agent():

    llm = get_llm()
    tools = get_all_tools()
    prompt = load_prompt("src/agent/prompts/agent_prompt.txt")  #

        # Initialize agent with memory checkpointing
    agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=prompt,
            checkpointer=memory_checkpointer  # Use the persistent checkpointer instance
        )

    return agent
