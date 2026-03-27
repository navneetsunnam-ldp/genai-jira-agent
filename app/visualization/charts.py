import plotly.express as px
import pandas as pd


def plot_velocity(data):
    if not isinstance(data, list) or not data:
        return None

    df = pd.DataFrame(data)

    if df.empty:
        return None

    return px.line(
        df,
        x="sprint",
        y="completed_issues",
        markers=True,
        title="Sprint Velocity"
    )


def plot_bug_trend(data):
    if not isinstance(data, list) or not data:
        return None

    df = pd.DataFrame(data)

    if df.empty or "date" not in df.columns:
        return None

    return px.line(
        df,
        x="date",
        y="count",
        markers=True,
        title="Bug Trend"
    )