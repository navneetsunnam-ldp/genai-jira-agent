import pandas as pd
from datetime import datetime


def run_analysis(query, data):
    query = query.lower()

    if any(x in query for x in ["velocity", "sprint", "performance"]):
        return calculate_velocity(data)

    elif any(x in query for x in ["cycle", "time"]):
        return calculate_cycle_time(data)

    elif any(x in query for x in ["bug", "defect"]):
        return calculate_bug_trend(data)

    return {"error": "Query not supported"}


def calculate_velocity(data):
    sprints = data.get("get_sprints", {}).get("values", [])

    closed = [s for s in sprints if s.get("state") == "closed"]
    last_sprints = closed[-6:]

    results = []

    for sprint in last_sprints:
        sid = sprint["id"]
        name = sprint["name"]

        issues = data.get(f"sprint_{sid}", {}).get("issues", [])

        completed = sum(
            1 for i in issues
            if i.get("fields", {}).get("status", {}).get("name", "").lower() == "done"
        )

        results.append({
            "sprint": name,
            "completed_issues": completed
        })

    return results


def calculate_cycle_time(data):
    issues = data.get("get_issues", {}).get("issues", [])

    times = []

    for issue in issues:
        histories = issue.get("changelog", {}).get("histories", [])

        for h in histories:
            for item in h.get("items", []):
                if item.get("field") == "status":
                    if item.get("toString") == "Done":
                        times.append(24)  # placeholder

    if not times:
        return {"error": "No cycle data"}

    return {"average_cycle_time_hours": sum(times) / len(times)}


def calculate_bug_trend(data):
    issues = data.get("get_issues", {}).get("issues", [])

    records = []

    for issue in issues:
        f = issue.get("fields", {})

        if f.get("issuetype", {}).get("name", "").lower() == "bug":
            created = f.get("created")
            if created:
                records.append({
                    "date": created.split("T")[0],
                    "count": 1
                })

    if not records:
        return {"error": "No bug data"}

    df = pd.DataFrame(records)
    df = df.groupby("date")["count"].sum().reset_index()

    return df.to_dict(orient="records")