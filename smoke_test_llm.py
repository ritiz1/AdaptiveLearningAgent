from app.ai.graph import build_graph


graph = build_graph()
question = "Help me understand AI agents"

for user_id in ["user-a", "user-b"]:
    result = graph.invoke(
        {
            "user_id": user_id,
            "session_id": f"session-{user_id}",
            "user_message": question,
        }
    )

    print(f"\n{'=' * 20} {user_id} {'=' * 20}")
    print(result["tutor_response"])