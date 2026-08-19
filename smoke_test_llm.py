from app.ai.graph import build_graph


graph = build_graph()
tests = [
    "Teach me Python recursion",
    "Help me review Python recursion",
    "Debug why my recursive function never stops",
]

for message in tests:
    result = graph.invoke({
        "user_id": "user-a",
        "session_id": "test-session",
        "user_message": message,
    })

    print("Message:", message)
    print("Intent:", result["intent"])
    print("Action:", result["next_action"])
    print("Response:", result["tutor_response"])
    print("-" * 50)