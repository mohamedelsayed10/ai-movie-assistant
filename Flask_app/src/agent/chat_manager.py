from langchain_core.messages import HumanMessage
from .agent_core import get_chat_agent
from ..utils.markdown_utils import convert_md_to_html

def run_chat_agent(prompt, thread_id, return_full_response=False):

    # Initialize chat agent
    chat_agent = get_chat_agent()
    
    # Prepare the message using LangChain message format
    messages = [HumanMessage(content=prompt)]
    
    response = chat_agent.invoke(
        {"messages": messages},
        {"configurable": {"thread_id": thread_id}}
    )

    # Convert markdown in the response to HTML for proper display in the UI
    response_content = response["messages"][-1].content
    html_response = convert_md_to_html(response_content)
    
    if return_full_response:
        # Return the full response structure for debugging
        return {
            "display_response": html_response,
            "full_response": response
        }
    else:
        # Return both the HTML response and the raw response for logging
        return html_response, response

