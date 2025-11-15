from langchain_core.prompts import PromptTemplate
from ..agent.llm_engine import get_llm


class PlotSummarizer:

    def __init__(self):
   
        
        # Initialize Gemini model
        self.llm = get_llm()
        
        # Define prompt template
        self.prompt = PromptTemplate(
            input_variables=["plot"],
            template=(
                "Summarize the following movie plot in 2-3 sentences without spoilers. "
                "Focus on the main premise and key characters while keeping the ending mysterious.\n\n"
                "Plot:\n{plot}\n\n"
                "Summary (2-3 sentences, no spoilers):"
            ),
        )
        
        # Create the chain
        self.chain = self.prompt | self.llm
        
    
    def summarize(self, plot_text):
        try:
            # Truncate very long plots (Gemini has context limits)
            max_length = 10000
            if len(plot_text) > max_length:
                plot_text = plot_text[:max_length] + "..."
            
            # Generate summary
            response = self.chain.invoke({"plot": plot_text})
            
            # Extract text from response
            if hasattr(response, 'content'):
                summary = response.content
            else:
                summary = str(response)
            
            # Clean up summary
            summary = summary.strip()
            
            return summary
        
        except Exception as e:
            print(f" Error summarizing plot: {e}")
            return f"Error: Unable to generate summary - {str(e)}"
    
  