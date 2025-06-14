import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import traceback

def run_python_code(code: str, namespace: dict = None) -> str:
    """
    Safely execute Python code and return the output.
    
    Args:
        code (str): Python code to execute
        namespace (dict): Namespace for the code execution
        
    Returns:
        str: Output of the code execution or error message
    """
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # Create a new namespace if none is provided
        if namespace is None:
            namespace = {}
        
        # Add builtins to namespace
        namespace.update({'__builtins__': __builtins__})
        
        # Execute code with the provided namespace
        exec(code, namespace)
        sys.stdout = old_stdout
        return redirected_output.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error executing code:\n{traceback.format_exc()}"
        
    finally:
        # Clean up
        redirected_output.close() 