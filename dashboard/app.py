from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from google.cloud import bigquery


REQUIRED_ENV_VARS = ("GCP_PROJECT_ID", "DBT_DATASET_NAME")
RPT_TABLES = {
    "departments": "rpt_department_summary",
    "aisles": "rpt_aisle_summary",
    "users": "rpt_user_order_summary",
}


st.set_page_config(
    page_title="Instacart Analytics Dashboard",
    layout="wide",
)


def _format_int(value: float | int | None) -> str:
    if pd.isna(value):
        return "0"
    return f"{int(value):,}"


def _format_pct(value: float | int | None) -> str:
    if pd.isna(value):
        return "0.0%"
    return f"{float(value) * 100:.1f}%"


def _format_float(value: float | int | None) -> str:
    if pd.isna(value):
        return "0.0"
    return f"{float(value):,.1f}"


def _check_configuration() -> tuple[str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if missing:
        st.error(
            "Missing environment variables: "
            + ", ".join(missing)
            + ". Set them before starting Streamlit."
        )
        st.stop()

    if credentials_path and not Path(credentials_path).exists():
        st.error(
            "GOOGLE_APPLICATION_CREDENTIALS points to a file that does not exist: "
            f"{credentials_path}"
        )
        st.stop()

    return os.environ["GCP_PROJECT_ID"], os.environ["DBT_DATASET_NAME"]


@st.cache_resource(show_spinner=False)
def get_bigquery_client(project_id: str) -> bigquery.Client:
    return bigquery.Client(project=project_id)


@st.cache_data(ttl=900, show_spinner=False)
def load_rpt_table(project_id: str, dataset_name: str, table_name: str) -> pd.DataFrame:
    client = get_bigquery_client(project_id)
    query = f"select * from `{project_id}.{dataset_name}.{table_name}`"
    return client.query(query).to_dataframe(create_bqstorage_client=False)


def load_data(project_id: str, dataset_name: str) -> dict[str, pd.DataFrame]:
    with st.spinner("Loading rpt tables from BigQuery..."):
        return {
            name: load_rpt_table(project_id, dataset_name, table)
            for name, table in RPT_TABLES.items()
        }


def render_kpis(departments: pd.DataFrame, aisles: pd.DataFrame, users: pd.DataFrame) -> None:
    total_line_items = departments["line_items"].sum()
    total_orders = departments["orders"].sum()
    total_users = users["user_id"].nunique()
    avg_reorder_rate = departments["reorder_rate"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Line items", _format_int(total_line_items))
    col2.metric("Orders", _format_int(total_orders))
    col3.metric("Users", _format_int(total_users))
    col4.metric("Avg reorder rate", _format_pct(avg_reorder_rate))

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Departments", _format_int(departments["department_id"].nunique()))
    col6.metric("Aisles", _format_int(aisles["aisle_id"].nunique()))
    col7.metric("Products", _format_int(departments["products"].sum()))
    col8.metric(
        "Avg cart position",
        _format_float(departments["avg_add_to_cart_position"].mean()),
    )


def render_department_tab(departments: pd.DataFrame, top_n: int, metric: str) -> None:
    st.subheader("Department Performance")
    chart_data = departments.sort_values(metric, ascending=False).head(top_n)
    st.bar_chart(chart_data, x="department", y=metric, use_container_width=True)

    display = departments.sort_values("line_items", ascending=False).copy()
    display["reorder_rate"] = display["reorder_rate"].map(_format_pct)
    display["avg_add_to_cart_position"] = display["avg_add_to_cart_position"].map(_format_float)
    st.dataframe(display, use_container_width=True, hide_index=True)


def render_aisle_tab(aisles: pd.DataFrame, departments: list[str], top_n: int, metric: str) -> None:
    st.subheader("Aisle Drilldown")
    filtered = aisles[aisles["department"].isin(departments)].copy()

    chart_data = filtered.sort_values(metric, ascending=False).head(top_n)
    st.bar_chart(chart_data, x="aisle", y=metric, color="department", use_container_width=True)

    display = filtered.sort_values("line_items", ascending=False)
    display["reorder_rate"] = display["reorder_rate"].map(_format_pct)
    display["avg_add_to_cart_position"] = display["avg_add_to_cart_position"].map(_format_float)
    st.dataframe(display, use_container_width=True, hide_index=True)


def render_user_tab(users: pd.DataFrame, min_orders: int) -> None:
    st.subheader("User Order Behavior")
    filtered = users[users["total_orders"] >= min_orders].copy()
    if filtered.empty:
        st.info("No users match the selected minimum order threshold.")
        return

    filtered["order_segment"] = pd.cut(
        filtered["total_orders"],
        bins=[0, 3, 10, 25, 1000],
        labels=["1-3 orders", "4-10 orders", "11-25 orders", "26+ orders"],
    )

    segment_summary = (
        filtered.groupby("order_segment", observed=True)
        .agg(
            users=("user_id", "nunique"),
            avg_total_orders=("total_orders", "mean"),
            avg_unique_products=("unique_products_ordered", "mean"),
            avg_reorder_rate=("reorder_rate", "mean"),
            avg_days_since_prior_order=("avg_days_since_prior_order", "mean"),
        )
        .reset_index()
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.bar_chart(segment_summary, x="order_segment", y="users", use_container_width=True)
    with col2:
        st.bar_chart(
            segment_summary,
            x="order_segment",
            y="avg_reorder_rate",
            use_container_width=True,
        )

    display = segment_summary.copy()
    display["avg_total_orders"] = display["avg_total_orders"].map(_format_float)
    display["avg_unique_products"] = display["avg_unique_products"].map(_format_float)
    display["avg_reorder_rate"] = display["avg_reorder_rate"].map(_format_pct)
    display["avg_days_since_prior_order"] = display["avg_days_since_prior_order"].map(_format_float)
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.caption("Top users by prior line items")
    top_users = filtered.sort_values("prior_line_items", ascending=False).head(100)
    st.dataframe(top_users, use_container_width=True, hide_index=True)


def main() -> None:
    project_id, dataset_name = _check_configuration()
    data = load_data(project_id, dataset_name)

    departments = data["departments"]
    aisles = data["aisles"]
    users = data["users"]

    st.title("Instacart Analytics Dashboard")
    st.caption(f"BigQuery source: `{project_id}.{dataset_name}`")

    metric_options = {
        "Line items": "line_items",
        "Orders": "orders",
        "Users": "users",
        "Products": "products",
        "Reorder rate": "reorder_rate",
        "Avg add-to-cart position": "avg_add_to_cart_position",
    }

    with st.sidebar:
        st.header("Filters")
        top_n = st.slider("Top rows", min_value=5, max_value=50, value=15, step=5)
        metric_label = st.selectbox("Rank by", list(metric_options), index=0)
        metric = metric_options[metric_label]
        selected_departments = st.multiselect(
            "Departments",
            sorted(aisles["department"].dropna().unique()),
            default=sorted(aisles["department"].dropna().unique()),
        )
        min_orders = st.slider("Minimum user orders", min_value=1, max_value=100, value=1)

    render_kpis(departments, aisles, users)

    overview_tab, department_tab, aisle_tab, user_tab = st.tabs(
        ["Overview", "Departments", "Aisles", "Users"]
    )

    with overview_tab:
        st.subheader("Where demand concentrates")
        col1, col2 = st.columns([1, 1])
        with col1:
            top_departments = departments.sort_values("line_items", ascending=False).head(top_n)
            st.bar_chart(top_departments, x="department", y="line_items", use_container_width=True)
        with col2:
            top_reorder = departments.sort_values("reorder_rate", ascending=False).head(top_n)
            st.bar_chart(top_reorder, x="department", y="reorder_rate", use_container_width=True)

    with department_tab:
        render_department_tab(departments, top_n, metric)

    with aisle_tab:
        render_aisle_tab(aisles, selected_departments, top_n, metric)

    with user_tab:
        render_user_tab(users, min_orders)


if __name__ == "__main__":
    main()
