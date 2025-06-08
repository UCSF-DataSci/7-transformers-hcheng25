import requests
import argparse
import os

def get_response(prompt, model_name="deepseek/deepseek-r1-0528-qwen3-8b", api_key=None):
    """
    Get a response from the model
    
    Args:
        prompt: The prompt to send to the model
        model_name: Name of the model to use
        api_key: API key for authentication (optional for some models)
        
    Returns:
        The model's response
    """
    # TODO: Implement the get_response function
    # Set up the API URL and headers
    # Create a payload with the prompt
    # Send the payload to the API
    # Extract and return the generated text from the response
    # Handle any errors that might occur
    # payload format based on what was found on the huggingface page of this model

    API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions" # using novita as inference provider
    if api_key != None:
        headers = {"Authorization": f"Bearer {api_key}"} # use api_key if inputted

    # code from query function in 02_llm_api_chat.ipynb
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": model_name
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()['choices'][0]['message']['content'] # try returning a more readable response; format is based on test
    except Exception as e:
        return f'Unexpected format: {e}\nFull response: {response}'

def run_chat(model_name="deepseek/deepseek-r1-0528-qwen3-8b", api_key=None):
    """Run an interactive chat session"""
    print("Welcome to the Simple LLM Chat! Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            response = get_response(prompt=user_input, model_name=model_name, api_key=api_key)
            print(response)
            break # break because one-off chat
        # TODO: Get response from the model
        # Print the response
        
def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM")
    # TODO: Add arguments to the parser
    parser.add_argument('-m', '--model', help = 'Specify model e.g. "deepseek/deepseek-r1-0528-qwen3-8b"')
    parser.add_argument('-k', '--key', help = 'Input API key if applicable')
    args = parser.parse_args()
    
    # TODO: Run the chat function with parsed arguments
    if args.model == None:
        args.model = "deepseek/deepseek-r1-0528-qwen3-8b" # set this model by default if no model specified
    run_chat(model_name=args.model, api_key=args.key)
    
if __name__ == "__main__":
    main()