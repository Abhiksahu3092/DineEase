# backend/agent.py
import json, re, os
from backend import tools
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Load single unified prompt
UNIFIED_PROMPT = open("prompts/unified_prompt.txt", encoding="utf-8").read()


def call_llm_api(messages, temperature=0.0):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=messages,
            temperature=temperature,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM API ERROR: {e}")
        return "I'm having trouble connecting right now."


def parse_tool_call(text):
    # Robust Regex to grab JSON even if wrapped in markdown
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return None
    return None


def run_agent_step(user_message, history):
    # Step 1: Create clean history with latest user message
    new_history = history.copy()
    new_history.append({"role": "user", "content": user_message})

    # Step 2: Use unified prompt for routing
    messages_for_router = [{"role": "system", "content": UNIFIED_PROMPT}] + new_history

    llm_out = call_llm_api(messages_for_router)
    tool_call = parse_tool_call(llm_out)

    if tool_call:
        tool_name = tool_call.get("tool")
        args = tool_call.get("args", {})

        try:
            if tool_name == "search_restaurants":
                result = tools.search_restaurants(**args)
            elif tool_name == "check_availability":
                result = tools.check_availability(**args)
            elif tool_name == "book_table":
                result = tools.book_table(**args)
            elif tool_name == "get_recommendations":
                result = tools.get_recommendations(**args)
            else:
                result = {"error": f"Unknown tool '{tool_name}'"}
        except Exception as e:
            result = {"error": str(e)}

        # Step 3: Summarize tool result using same unified prompt
        summary_history = new_history + [
            {"role": "assistant", "content": json.dumps(tool_call)},
            {"role": "system", "content": f"TOOL_RESULT: {json.dumps(result)}"},
        ]

        messages_for_summary = [
            {"role": "system", "content": UNIFIED_PROMPT}
        ] + summary_history
        final_reply = call_llm_api(messages_for_summary)

        # Don't modify the passed history parameter - app.py will handle it
        return final_reply, result

    else:
        # No tool call, direct LLM reply
        return llm_out, None
