import argparse
import os
from logging import raiseExceptions

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API Key could not be found")

    client = genai.Client(api_key=api_key)
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if response.candidates:
            for item in response.candidates:
                messages.append(item.content)

        usage = response.usage_metadata

        if usage is None:
            raise RuntimeError("Failed API request on usage metadata")
        if args.verbose is True:
            print("User prompt:", args.user_prompt)
            print("Prompt tokens:", usage.prompt_token_count)
            print("Response tokens:", usage.candidates_token_count)
        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception(f"Function {function_call.name} returned no result")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception(
                        f"Function {function_call.name} returned no response"
                    )
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
            messages.append(types.Content(role="user", parts=function_results))

        else:
            print("Response:")
            print(response.text)
            break
    else:
        print("Reached maximum number of iterations")
        sys.exit(1)


if __name__ == "__main__":
    main()

""" if len(sys.argv) != 2:
        print('Please provide a prompt in the form of "Text ..." for the AI model')
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]"""
