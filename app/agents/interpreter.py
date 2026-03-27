import ollama
import re


# Get semantic understanding from LLM
def get_llm_understanding(user_query):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the intent of this Jira query in one short sentence."
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )

        return response["message"]["content"].lower()

    except:
        return user_query.lower()


# Extract time range dynamically
def extract_time_range(text):
    sprint_match = re.search(r'last\s+(\d+)\s+sprint', text)
    if sprint_match:
        return f"last_{sprint_match.group(1)}_sprints"

    week_match = re.search(r'last\s+(\d+)\s+week', text)
    if week_match:
        return f"last_{week_match.group(1)}_weeks"

    if "last month" in text:
        return "last_1_month"

    if "current sprint" in text:
        return "current_sprint"

    return ""


# Extract intent + metrics dynamically
def extract_intent_and_metrics(text):
    result = {
        "intent": "unknown",
        "metrics": [],
        "group_by": "",
        "filters": {}
    }

    # semantic matching

    if "velocity" in text:
        result["intent"] = "sprint_velocity"
        result["metrics"].append("velocity")
        result["group_by"] = "sprint"

    elif "cycle time" in text:
        result["intent"] = "cycle_time"
        result["metrics"].append("cycle_time")
        result["group_by"] = "issue_type"

    elif "bug" in text:
        result["intent"] = "bug_trend"
        result["metrics"].append("bugs")
        result["group_by"] = "sprint"

    elif "burndown" in text:
        result["intent"] = "burndown"

    elif "in progress" in text or "in-progress" in text:
        result["intent"] = "workload_distribution"
        result["filters"]["status"] = "in_progress"
        result["group_by"] = "assignee"

    elif "epic" in text and ("risk" in text or "delay" in text):
        result["intent"] = "risk_detection"

    return result


# MAIN FUNCTION
def interpret_query(user_query: str):
    combined_text = user_query.lower()

    # Step 1: LLM understanding (adds semantic strength)
    llm_text = get_llm_understanding(user_query)

    combined_text += " " + llm_text

    # Step 2: Extract components
    time_range = extract_time_range(combined_text)
    intent_data = extract_intent_and_metrics(combined_text)

    # Step 3: Build final structured output
    result = {
        "intent": intent_data["intent"],
        "project": "BC72",
        "time_range": time_range,
        "metrics": intent_data["metrics"],
        "filters": intent_data["filters"],
        "group_by": intent_data["group_by"]
    }

    return result