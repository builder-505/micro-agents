"""
Recipe 01: Single-Loop Tool-Calling Agent
Lines of code: ~65
Zero framework dependencies.

Demonstrates:
- How LLM tool calling works under the hood
- Schema declaration
- Tool execution dispatch
- Feeding tool response back into message history
"""

import os
import sys
import json
import urllib.request

# Ensure UTF-8 output across all operating systems and terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1. Define custom tools (plain Python functions)
def get_stock_price(symbol: str) -> str:
    """Mock stock price lookup."""
    prices = {"AAPL": "$230.50", "NVDA": "$135.20", "GOOG": "$182.10", "TSLA": "$248.90"}
    return json.dumps({"symbol": symbol.upper(), "price": prices.get(symbol.upper(), "Unknown")})

def calculate_roi(initial: float, current: float) -> str:
    """Calculate percentage return on investment."""
    roi = ((current - initial) / initial) * 100
    return json.dumps({"initial": initial, "current": current, "roi_percent": f"{roi:.2f}%"})

AVAILABLE_TOOLS = {
    "get_stock_price": get_stock_price,
    "calculate_roi": calculate_roi,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Fetch current market price for a stock ticker symbol",
            "parameters": {
                "type": "object",
                "properties": {"symbol": {"type": "string", "description": "Ticker symbol, e.g. AAPL"}},
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_roi",
            "description": "Calculate return on investment percentage",
            "parameters": {
                "type": "object",
                "properties": {
                    "initial": {"type": "number"},
                    "current": {"type": "number"}
                },
                "required": ["initial", "current"]
            }
        }
    }
]

def call_llm(messages, api_key=None):
    """Simple HTTP call to OpenAI-compatible API or fallback to mock simulation."""
    if not api_key:
        # Offline simulation mode for instant zero-config testing
        last_msg = messages[-1]
        if last_msg["role"] == "user":
            return {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": "call_01",
                    "type": "function",
                    "function": {"name": "get_stock_price", "arguments": json.dumps({"symbol": "NVDA"})}
                }]
            }
        elif last_msg["role"] == "tool":
            return {
                "role": "assistant",
                "content": "The current price of NVDA is $135.20 based on market data.",
                "tool_calls": None
            }

    url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    payload = json.dumps({"model": "gpt-4o-mini", "messages": messages, "tools": TOOL_SCHEMAS}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]

def run_agent_loop(user_prompt: str, max_turns: int = 5):
    api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        {"role": "system", "content": "You are a helpful financial assistant with tool access."},
        {"role": "user", "content": user_prompt}
    ]

    print(f"\n👤 User: {user_prompt}\n" + "-"*50)
    for turn in range(max_turns):
        print(f"🔄 Loop Turn {turn + 1}...")
        assistant_msg = call_llm(messages, api_key)
        messages.append(assistant_msg)

        tool_calls = assistant_msg.get("tool_calls")
        if not tool_calls:
            print(f"🤖 Agent Final Response:\n{assistant_msg.get('content')}")
            break

        for tc in tool_calls:
            tool_name = tc["function"]["name"]
            tool_args = json.loads(tc["function"]["arguments"])
            print(f"  🛠️ Invoking Tool: {tool_name}({tool_args})")
            
            tool_fn = AVAILABLE_TOOLS.get(tool_name)
            result = tool_fn(**tool_args) if tool_fn else json.dumps({"error": "tool not found"})
            print(f"  📥 Tool Output: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "name": tool_name,
                "content": result
            })

if __name__ == "__main__":
    run_agent_loop("What is the current stock price of NVDA?")
