"""
Recipe 02: ReAct (Reasoning + Acting) Agent
Lines of code: ~75
Zero framework dependencies.

Demonstrates:
- The fundamental ReAct loop (Thought -> Action -> Observation)
- Regex-based action parsing
- Stop token simulation & step-by-step reasoning
"""

import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Simulated Knowledge Base / External Tools
WIKI_DB = {
    "james webb space telescope": "The JWST was launched on 25 December 2021 aboard an Ariane 5 rocket from Kourou, French Guiana.",
    "kourou": "Kourou is a commune in French Guiana, an overseas region and department of France in South America.",
    "ariane 5": "Ariane 5 is a retired European heavy-lift space launch vehicle developed by Arianespace."
}

def search_wiki(query: str) -> str:
    query = query.strip().lower()
    for key, text in WIKI_DB.items():
        if key in query or query in key:
            return text
    return "No match found in knowledge base."

ACTIONS = {
    "search": search_wiki
}

PROMPT_TEMPLATE = """Answer the question using the following format:

Thought: reason about what step to take next.
Action: tool_name[argument]
Observation: result of the tool
... (repeat Thought/Action/Observation as needed)
Thought: I now have the final answer.
Final Answer: the conclusive answer to the original question.

Available tools:
- search[query]: Searches the knowledge base for a topic.

Question: {question}
"""

def mock_llm_step(prompt: str) -> str:
    """Simulates an LLM generating one step of the ReAct sequence."""
    if "Observation: The JWST was launched on 25 December 2021" in prompt:
        return (
            "Thought: The launch vehicle was an Ariane 5 and the location was Kourou, French Guiana. "
            "I now know the launch date and location.\n"
            "Final Answer: The James Webb Space Telescope was launched on December 25, 2021 from Kourou, French Guiana."
        )
    return (
        "Thought: I need to find when and from where the James Webb Space Telescope was launched.\n"
        "Action: search[james webb space telescope]"
    )

def run_react_agent(question: str, max_iterations: int = 5):
    print(f"\n❓ Question: {question}\n" + "="*50)
    history = PROMPT_TEMPLATE.format(question=question)

    for i in range(max_iterations):
        print(f"\n📍 Iteration {i+1}:")
        llm_response = mock_llm_step(history)
        history += llm_response

        # Check for Final Answer
        if "Final Answer:" in llm_response:
            final_answer = llm_response.split("Final Answer:")[-1].strip()
            thought = llm_response.split("Final Answer:")[0].strip()
            print(f"💭 {thought}")
            print(f"\n🎯 [FINAL ANSWER]: {final_answer}")
            return final_answer

        # Parse Action: tool_name[arg]
        action_match = re.search(r"Action:\s*(\w+)\[(.*?)\]", llm_response)
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", llm_response, re.DOTALL)

        if thought_match:
            print(f"💭 Thought: {thought_match.group(1).strip()}")

        if action_match:
            tool_name = action_match.group(1).strip()
            tool_arg = action_match.group(2).strip()
            print(f"⚡ Action: {tool_name}('{tool_arg}')")

            tool_fn = ACTIONS.get(tool_name)
            observation = tool_fn(tool_arg) if tool_fn else "Unknown tool"
            print(f"👁️ Observation: {observation}")

            history += f"\nObservation: {observation}\n"
        else:
            print("⚠️ No valid action parsed.")
            break

if __name__ == "__main__":
    run_react_agent("When and from where was the James Webb Space Telescope launched?")
