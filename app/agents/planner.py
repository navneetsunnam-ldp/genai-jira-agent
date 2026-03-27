def plan_query(query_json):
    intent = query_json.get("intent")

    if intent == "sprint_velocity":
        return {
            "steps": [
                {"action": "get_sprints"},
                {"action": "get_issues", "params": {"type": "sprint"}},
                {"action": "compute_velocity"}
            ]
        }

    elif intent == "cycle_time":
        return {
            "steps": [
                {"action": "get_issues"},
                {"action": "compute_cycle_time"}
            ]
        }

    elif intent == "bug_trend":
        return {
            "steps": [
                {"action": "get_issues", "params": {"issue_type": "bug"}},
                {"action": "aggregate_trend"}
            ]
        }

    elif intent == "workload_distribution":
        return {
            "steps": [
                {"action": "get_issues"},
                {"action": "group_by_assignee"}
            ]
        }

    return {"steps": []}