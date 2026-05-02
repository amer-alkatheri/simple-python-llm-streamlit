import os
from openai import OpenAI
from dotenv import load_dotenv

from agent import get_stock_price
from agent import tools_list

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def main_agent():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. When you need to use a tool, use the built-in tool-calling feature. Do not write the function call yourself in text."
        }
    ]

    while True:
        input_text = input("You: ")

        messages.append({
            "role": "user",
            "content": input_text
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,

            tools=tools_list,
            tool_choice="auto"
        )

        response_from_ai = response.choices[0].message
        
        tool_calls = response_from_ai.tool_calls
        # print(f"Tools are: {tool_calls}")

        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                # If AI wants stock price:
                if function_name == "get_stock_price":
                    import json
                    args = json.loads(tool_call.function.arguments)
                    result = get_stock_price(args.get("symbol"))

                    response_from_tool_calls = {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": result,
                    }

                    messages.append(response_from_tool_calls)

                second_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages
                )
                
                print (second_response.choices[0].message.content)
        else:
            print(response_from_ai.content)


def main_ui(messages):

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,

            tools=tools_list,
            tool_choice="auto"
        )

        response_from_ai = response.choices[0].message
        
        tool_calls = response_from_ai.tool_calls
        # print(f"Tools are: {tool_calls}")

        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                # If AI wants stock price:
                if function_name == "get_stock_price":
                    import json
                    args = json.loads(tool_call.function.arguments)
                    result = get_stock_price(args.get("symbol"))

                    response_from_tool_calls = {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": result,
                    }

                    messages.append(response_from_tool_calls)

                second_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages
                )
                
                return (second_response.choices[0].message.content)
        else:
            return(response_from_ai.content)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    main_agent()