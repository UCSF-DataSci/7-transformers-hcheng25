import requests
import argparse
import os

def get_response(prompt, model_name="deepseek/deepseek-r1-0528-qwen3-8b", api_key=None, history=[]):
    """
    Get a response from the model using conversation history
    
    Args:
        prompt: The current user prompt
        history: List of previous (prompt, response) tuples
        model_name: Name of the model to use
        api_key: API key for authentication
        history_length: Number of previous exchanges to include in context
        
    Returns:
        The model's response
    """
    # TODO: Format a prompt that includes previous exchanges
    # Get a response from the API
    # Return the response

    # payload format based on what was found on the huggingface page of this model

    API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions" # using novita as inference provider
    if api_key != None:
        headers = {"Authorization": f"Bearer {api_key}"} # use api_key if inputted

    history.append({'role':'user', 'content':prompt}) # add the current input to the history
    
    payload = {
        "messages": history, # submit history to model
        "model": model_name
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    history.append({'role': 'assistant', 'content':response.json()['choices'][0]['message']['content']}) # append the response to the history

    try:
        return response.json()['choices'][0]['message']['content'], history # output both response and history
    except Exception as e:
        return f'Unexpected format: {e}\nFull response: {response}'

def run_chat(model_name="deepseek/deepseek-r1-0528-qwen3-8b", api_key=None, history_len=2):
    """Run an interactive chat session"""
    history = [] # initialize empty history
    print("Welcome to the Contextual LLM Chat! Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            response, history = get_response(prompt=user_input, model_name=model_name, api_key=api_key, history=history)
            print(response)
            while len(history)>history_len*2: # note: history_len is number of _exchanges_ not messages
                history.pop(0) # remove earliest messages until history length is below specified limit
        # TODO: Get response from the model
        # Print the response
        
def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM")
    # TODO: Add arguments to the parser
    parser.add_argument('-m', '--model', help = 'Specify model e.g. "deepseek/deepseek-r1-0528-qwen3-8b"')
    parser.add_argument('-k', '--key', help = 'Input API key if applicable')
    parser.add_argument('-l', '--length', help = 'Number of exchanges to save in history during session')
    args = parser.parse_args()
    
    # TODO: Run the chat function with parsed arguments
    if args.model == None:
        args.model = "deepseek/deepseek-r1-0528-qwen3-8b" # set this model by default if no model specified
    if args.length == None:
        args.length = 2 # default save 2 exchanges in history during chat
    run_chat(model_name=args.model, api_key=args.key, history_len=args.length)
    
if __name__ == "__main__":
    main()