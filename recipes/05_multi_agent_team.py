"""
Recipe 05: Multi-Agent Supervisor & Worker Team
Lines of code: ~90
Zero framework dependencies.

Demonstrates:
- Supervisor / Orchestrator routing pattern
- Specialized worker agent personas (Researcher + Technical Writer)
- Handoff mechanics and context aggregation
"""

import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Simulated specialized workers
def researcher_agent(topic: str) -> dict:
    """Specialist focused on factual data discovery."""
    print(f"  🔍 [Researcher Agent] Gathering deep technical points on: '{topic}'")
    return {
        "key_facts": [
            "SQLite is serverless and self-contained in a single disk file.",
            "Supports full ACID compliance even across system crashes.",
            "Processes billions of queries daily inside Android, iOS, Chrome, and Python standard library."
        ],
        "latency_profile": "Sub-millisecond local reads, zero network overhead."
    }

def writer_agent(research_data: dict) -> str:
    """Specialist focused on developer-facing technical communication."""
    print("  ✍️ [Technical Writer Agent] Formatting findings into punchy developer post...")
    facts = "\n".join([f"- {f}" for f in research_data["key_facts"]])
    return (
        f"### Why SQLite Still Dominates Modern Architecture\n\n"
        f"{facts}\n\n"
        f"**Performance Note**: {research_data['latency_profile']}\n"
        f"**Conclusion**: Before spinning up a distributed cluster, benchmark embedded SQLite first."
    )

def supervisor_agent(user_request: str) -> str:
    """Supervisor orchestrates the team pipeline."""
    print(f"\n👔 [Supervisor Agent] Received mission: '{user_request}'")
    print("  ↳ Step 1: Assigning investigation to Researcher Agent...")
    findings = researcher_agent(user_request)

    print("  ↳ Step 2: Routing findings to Writer Agent...")
    article = writer_agent(findings)

    print("  ↳ Step 3: Performing quality assurance review...")
    return article

if __name__ == "__main__":
    mission = "Why SQLite is the unsung hero of production software"
    final_post = supervisor_agent(mission)
    print("\n📦 Final Deliverable from Agent Team:\n" + "="*50)
    print(final_post)
