import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

class ClaudeClient:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        self.client = Anthropic()

    def generate_response(self, prompt, max_tokens=1000):
        """
        Generate a response using Claude 3 Sonnet
        
        Args:
            prompt (str): The input prompt for Claude
            max_tokens (int): Maximum number of tokens in the response
            
        Returns:
            str: Claude's response
        """
        try:
            message = self.client.beta.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    try:
        claude = ClaudeClient()
        response = claude.generate_response("Hello! How are you today?")
        print("Claude's response:", response)
    except ValueError as e:
        print(e) 