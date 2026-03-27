import ollama
import json


def prepare_context(data):
    """
    Reduce noise but keep useful structure
    """
    context = {}

    #  Sprints
    sprints = data.get("get_sprints", {}).get("values", [])
    context["sprints"] = [
        {
            "id": s["id"],
            "name": s["name"],
            "state": s["state"]
        }
        for s in sprints
    ]

    #  Issues (limit for token safety)
    issues = data.get("get_issues", {}).get("issues", [])[:50]

    context["issues"] = [
        {
            "type": i.get("fields", {}).get("issuetype", {}).get("name"),
            "status": i.get("fields", {}).get("status", {}).get("name"),
            "created": i.get("fields", {}).get("created"),
            "assignee": (
                i.get("fields", {}).get("assignee", {}).get("displayName")
                if i.get("fields", {}).get("assignee") else "Unassigned"
            )
        }
        for i in issues
    ]

    return context


def generate_insight(query, data):
    try:
        context = prepare_context(data)

        context_str = json.dumps(context, indent=2)

        prompt = f"""
You are a senior Jira analytics expert.

User Question:
{query}

Jira Context:
{context_str}

Instructions:
- Understand the user's question deeply
- Decide what metric is needed (velocity, bugs, cycle time, workload, etc.)
- Analyze the data yourself
- Do NOT assume anything
- Do NOT give generic answers
- Use specific observations from data
- Answer in 2–4 lines
- Be precise and insightful

Answer:
"""

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.get("message", {}).get("content", "").strip()

        if content:
            return content

    except Exception as e:
        return f"LLM Error: {str(e)}"

    return "Unable to generate insight."