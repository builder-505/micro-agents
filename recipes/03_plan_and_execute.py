"""
Recipe 03: Plan-and-Execute Agent
Lines of code: ~85
Zero framework dependencies.

Demonstrates:
- Decoupling high-level strategic planning from low-level execution
- Generating an ordered step checklist
- Stepwise execution with state blackboard accumulation
- Handling multi-step research and synthesis workflows
"""

import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Simulated subtask tools
def gather_metrics(topic: str) -> str:
    return "Global AI compute demand increased 4.2x year-over-year in 2024."

def analyze_trend(metrics: str) -> str:
    return "Surge driven primarily by open-source inference and multi-modal edge devices."

def format_summary(data: dict) -> str:
    return f"Executive Briefing:\n- Data Point: {data.get('metrics')}\n- Strategic Takeaway: {data.get('trend')}"

EXECUTOR_TOOLS = {
    "gather_metrics": gather_metrics,
    "analyze_trend": analyze_trend,
    "format_summary": format_summary
}

def planner(goal: str) -> list[dict]:
    """Generates an actionable execution plan of subtasks."""
    print(f"📋 Planner analyzing objective: '{goal}'...")
    # In live mode, this is generated via structured JSON LLM output:
    return [
        {"id": 1, "task": "Fetch compute growth metrics", "tool": "gather_metrics", "input": "AI compute"},
        {"id": 2, "task": "Analyze growth drivers", "tool": "analyze_trend", "input": "$output_1"},
        {"id": 3, "task": "Synthesize executive report", "tool": "format_summary", "input": "$blackboard"}
    ]

def executor(plan: list[dict]) -> str:
    """Executes the plan sequentially, passing context through a blackboard."""
    blackboard = {}
    print("\n🚀 Executing Plan Steps:")

    for step in plan:
        step_id = step["id"]
        tool_name = step["tool"]
        raw_input = step["input"]

        # Resolve inputs from earlier steps
        if raw_input == "$output_1":
            actual_input = blackboard.get(1, "")
        elif raw_input == "$blackboard":
            actual_input = {"metrics": blackboard.get(1), "trend": blackboard.get(2)}
        else:
            actual_input = raw_input

        print(f"  [Step {step_id}] {step['task']} -> calling '{tool_name}'")
        tool_fn = EXECUTOR_TOOLS[tool_name]
        result = tool_fn(actual_input)
        blackboard[step_id] = result
        print(f"    ↳ Output: {result[:60]}...")

    return blackboard[plan[-1]["id"]]

def run_plan_and_execute(goal: str):
    print(f"\n🎯 High-Level Goal: {goal}\n" + "="*50)
    plan = planner(goal)
    for p in plan:
        print(f"  [{p['id']}] {p['task']} (tool: {p['tool']})")
    
    final_output = executor(plan)
    print("\n🏁 Final Synthesized Result:\n" + "-"*50)
    print(final_output)

if __name__ == "__main__":
    run_plan_and_execute("Create an executive briefing on 2024 AI compute growth.")
