import streamlit as st
from app.mcp.jira_client import call_mcp
from app.analytics.engine import run_analysis
from app.visualization.charts import plot_velocity, plot_bug_trend
from app.agents.insight import generate_insight

st.set_page_config(page_title="GenAI Jira Agent", layout="wide")

st.title("🚀 GenAI Jira Agent")

query = st.text_input("💬 Ask a Jira question:")

if st.button("Run Query"):

    if not query.strip():
        st.warning("Enter a query")

    else:
        results = {}

        # 🔥 FETCH ALL DATA
        results["get_sprints"] = call_mcp("get_sprints")
        results["get_issues"] = call_mcp("get_issues")

        sprints = results["get_sprints"].get("values", [])
        closed = [s for s in sprints if s.get("state") == "closed"]
        last_sprints = closed[-6:]

        for sprint in last_sprints:
            sid = sprint["id"]
            results[f"sprint_{sid}"] = call_mcp(
                "get_issues_by_sprint",
                {"sprint_id": sid}
            )

        # 🔥 ANALYTICS (ONLY FOR VISUALIZATION)
        analysis = run_analysis(query, results)

        # 🔥 VISUALIZATION
        st.subheader("📊 Visualization")

        fig = None

        if isinstance(analysis, list) and analysis:
            if "completed_issues" in analysis[0]:
                fig = plot_velocity(analysis)

            elif "count" in analysis[0]:
                fig = plot_bug_trend(analysis)

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No visualization available")

        # 🔥 LLM INSIGHT (RAW DATA BASED)
        st.subheader("🧠 Insight Summary")

        insight = generate_insight(query, results)  # 🔥 IMPORTANT CHANGE

        st.success(insight)