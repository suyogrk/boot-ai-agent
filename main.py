from google.genai import types
from google import genai
from google.genai.types import GenerateContentResponse 
from dotenv import load_dotenv
import os
import argparse
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError('Api key not found')

client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response: GenerateContentResponse = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
         config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
        )
    
    usage_metadata = response.usage_metadata

    if usage_metadata is None:
        raise RuntimeError('Api failed')
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
    
    print(response.text)
    function_calls = response.function_calls

    if function_calls is not None:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

if __name__ == "__main__":
    main()