from google.genai.types import Candidate
from call_function import call_function
from google.genai import types
from google import genai
from google.genai.types import GenerateContentResponse,  Content , FunctionResponse
from dotenv import load_dotenv
import os
import argparse
from prompts import system_prompt
from call_function import available_functions
from config import GEMINI_2_5_FLASH, GEMINI_2_5_FLASH_LITE, GEMINI_3_FLASH, GEMINI_2_0_FLASH_LITE

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

    for _ in range(20):
        response: GenerateContentResponse = client.models.generate_content(
            model=GEMINI_2_5_FLASH,
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
            )
        
        response_candidates: list[Candidate]| None = response.candidates


        if response_candidates is not None:
            for candidate in response_candidates:
                if candidate.content:
                    messages.append(candidate.content)
        
        usage_metadata = response.usage_metadata

        if usage_metadata is None:
            raise RuntimeError('Api failed')
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
            print(f"Response tokens: {usage_metadata.candidates_token_count}")
        
        function_calls = response.function_calls

        function_result_list = []

        if function_calls is None:
            print(response.text)
            return

        if function_calls is not None:
            for function_call in function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result: Content = call_function(function_call)

                if not function_call_result.parts:
                    raise Exception('parts not found in function call result')

                function_response: FunctionResponse | None = function_call_result.parts[0].function_response

                if function_response is None:
                    raise Exception("function response is none")
                
                actual_response = function_response.response

                if actual_response is None:
                    raise Exception("There is no response")

                function_result_list.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {actual_response}")

        for result in function_result_list:
            messages.append(types.Content(
            role="user",
            parts=[
                types.Part(
                    text=result.text,
                    function_response=result.function_response,
                    thought=getattr(result, "thought_signature", None)  # preserve it
                )]))
    exit(-1)
        

if __name__ == "__main__":
    main()