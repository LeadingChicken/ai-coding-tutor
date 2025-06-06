import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import traceback

def run_python_code(code: str) -> str:
    """
    Safely execute Python code and return the output.
    
    Args:
        code (str): Python code to execute
        
    Returns:
        str: Output of the code execution or error message
    """
    # Create string buffers for stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    try:
        # Redirect stdout and stderr to our buffers
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            # Create a single namespace for both global and local variables
            namespace = {}
            
            # Execute the code in the namespace
            exec(code, namespace)
            
        # Get output and errors
        output = stdout_buffer.getvalue()
        errors = stderr_buffer.getvalue()
        
        # Combine output and errors
        result = output
        if errors:
            result += f"\nErrors:\n{errors}"
            
        return result if result.strip() else "Code executed successfully with no output."
        
    except Exception as e:
        # Get the full traceback but skip the first frame which is our execution code
        error_lines = traceback.format_exc().splitlines()
        # Remove internal execution details
        filtered_lines = [line for line in error_lines if 'File "<string>"' in line or not line.startswith('  File ')]
        error_msg = '\n'.join(filtered_lines)
        return f"Error executing code:\n{error_msg}"
        
    finally:
        # Clean up
        stdout_buffer.close()
        stderr_buffer.close() 