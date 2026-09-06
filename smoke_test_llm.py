from app.ai.graph.build_graph import build_graph
import logging
import sys

logging.basicConfig(level=logging.INFO)

# LLM output contains characters the default Windows console cannot encode.
sys.stdout.reconfigure(encoding="utf-8")

graph = build_graph()

# Both users run the same prompts so personalization differences are visible.
users = ["user-a", "user-b"]
tests = [
    "Teach me Python recursion",
    "Help me review Python recursion",
    "Debug why my recursive function never stops. ",
]

for user_id in users:
    print("=" * 50)
    print("User:", user_id)
    print("=" * 50)

    for message in tests:
        result = graph.invoke({
            "user_id": user_id,
            "session_id": f"test-session-{user_id}",
            "user_message": message,
        })

        print("Message:", message)
        print("Intent:", result["intent"])
        print("Action:", result["next_action"])
        print("Response:", result["tutor_response"])
        print("-" * 50)
