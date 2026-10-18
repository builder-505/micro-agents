"""
Recipe 04: Self-Reflection & Auto-Healing Code Agent
Lines of code: ~80
Zero framework dependencies.

Demonstrates:
- The "Reflexion" feedback loop (Draft -> Execute -> Inspect Error -> Reflect -> Patch)
- Running dynamic code in a subprocess sandbox
- Automatic error recovery without human intervention
"""

import sys
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TEST_SUITE = """
assert reverse_words("hello world") == "world hello"
assert reverse_words("ai agents rock") == "rock agents ai"
assert reverse_words("") == ""
print("ALL_TESTS_PASSED")
"""

# Simulated iterative code revisions from LLM
CODE_REVISIONS = [
    # Attempt 1: Has an intentional bug (AttributeError on reverse())
    """
def reverse_words(s: str) -> str:
    words = s.split(" ")
    return words.reverse()
""",
    # Attempt 2: Has an intentional bug (returns list instead of joined string)
    """
def reverse_words(s: str) -> str:
    if not s: return ""
    return s.split()[::-1]
""",
    # Attempt 3: Fixed solution
    """
def reverse_words(s: str) -> str:
    if not s.strip(): return ""
    return " ".join(s.split()[::-1])
"""
]

def run_code_in_sandbox(code_str: str) -> tuple[bool, str]:
    """Executes generated code against unit tests in a subprocess."""
    full_script = code_str + "\n" + TEST_SUITE
    try:
        proc = subprocess.run(
            [sys.executable, "-c", full_script],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode == 0 and "ALL_TESTS_PASSED" in proc.stdout:
            return True, "Success! All unit tests passed."
        return False, proc.stderr.strip() or proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Execution timed out."

def run_reflection_agent(max_attempts: int = 3):
    print("\n🛠️ Objective: Write a function `reverse_words(s: str) -> str` that passes all tests.")
    print("="*65)

    last_error = "Initial generation"
    for attempt in range(max_attempts):
        print(f"\n🔁 Attempt {attempt + 1}/{max_attempts}:")
        code_draft = CODE_REVISIONS[attempt]
        print(f"Generated Code:\n{code_draft.strip()}")

        passed, output = run_code_in_sandbox(code_draft)

        if passed:
            print(f"\n🎉 Test Suite Result: {output}")
            print("✅ Verified Working Code Produced!")
            return code_draft
        else:
            print(f"\n❌ Execution Failed!")
            print(f"Stderr Traceback:\n  {output}")
            print(f"💡 Reflection: Identified failure in test runner. Feeding traceback back to LLM to self-heal...")
            last_error = output

    print("\n⚠️ Agent reached max attempts without resolution.")

if __name__ == "__main__":
    run_reflection_agent()
