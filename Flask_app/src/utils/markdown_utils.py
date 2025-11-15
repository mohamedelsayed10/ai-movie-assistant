import markdown

def convert_md_to_html(markdown_text):
    """
    Convert markdown text to HTML for display in the chatbot UI
    """
    # Configure markdown with extensions for better formatting
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',  # Includes tables, fenced code blocks, etc.
            'markdown.extensions.codehilite',  # Syntax highlighting
            'markdown.extensions.toc',  # Table of contents
            'markdown.extensions.nl2br',  # New line to <br>
        ]
    )
    
    html = md.convert(markdown_text)
    return html