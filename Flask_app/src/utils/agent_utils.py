import io
import sys

def serialize_message(msg):
    """Serialize a message object using pretty_print if available"""
    # Try to use pretty_print() if the message has it
    if hasattr(msg, 'pretty_print'):
        try:
            # Capture pretty_print output
            
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            msg.pretty_print()
            
            sys.stdout = old_stdout
            pretty_output = captured_output.getvalue()
            
            return {
                "pretty_print": pretty_output,
                "type": type(msg).__name__
            }
        except Exception as e:
            return {
                "content": str(msg),
                "type": type(msg).__name__
            }
           
    
    # Fallback to manual serialization
    raw_msg = {}
    
    # Always include content
    if hasattr(msg, 'content'):
        raw_msg["content"] = msg.content
    else:
        raw_msg["content"] = str(msg)
    
    # Include other common attributes if they exist
    if hasattr(msg, 'type'):
        raw_msg["type"] = type(msg).__name__
    
    if hasattr(msg, 'role'):
        raw_msg["role"] = msg.role
        
    if hasattr(msg, 'name'):
        raw_msg["name"] = msg.name
        
    if hasattr(msg, 'additional_kwargs'):
        raw_msg["additional_kwargs"] = str(msg.additional_kwargs)
        
    if hasattr(msg, 'id'):
        raw_msg["id"] = msg.id
    
    # Tool calls if available
    if hasattr(msg, 'tool_calls'):
        raw_msg["tool_calls"] = str(msg.tool_calls)
    
    # Response metadata if available
    if hasattr(msg, 'response_metadata'):
        raw_msg["response_metadata"] = str(msg.response_metadata)
    
    return raw_msg



ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'webm', 'm4a'}
def allowed_file(filename: str) -> bool:
    """Check if uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
