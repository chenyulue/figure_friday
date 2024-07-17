import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import streamlit as st

import assets

st.set_page_config(
    page_title="Figure Friday 2024, Week 28",
    layout="wide",
)

sale_color = "#fc8d59"
negative_color = "#d7191c"
positive_color = "#2c7bb6"
light_gray = "#C4C4C4"

@st.cache_data
def load_data():
    return pd.read_excel(assets.DATA24_WK28, parse_dates=["Order Date"])

@st.cache_data
def get_figure_for_category():
    df24_wk28 = load_data()
    df24_wk28_filtered = df24_wk28.loc[:, ["Category", "Sales", "Profit"]].groupby(
        by="Category"
    ).sum().sort_values(by="Sales", ascending=False)

    fig = px.bar(
        df24_wk28_filtered.reset_index(),
        x="Category",
        y=df24_wk28_filtered.columns,
        barmode="group",
    )

    fig.update_traces(
        selector=dict(name="Sales"),
        marker_color=sale_color,
        hovertemplate="<b>Sales</b><br>%{x}: <b>%{y:$,.0f}</b><extra></extra>"
    )
    fig.update_traces(
        selector=dict(name="Profit"),
        marker_color=positive_color,
        hovertemplate="<b>Profit</b><br>%{x}: <b>%{y:$,.0f}</b><extra></extra>"
    )
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="white",
        )
    )

    fig.add_annotation(
        text=("The sales of furniture are ranked second, but the profit <br>of that is the least."),
        x=0, xref="paper", xanchor="left",
        y=1, yref="paper", yanchor="bottom",
        yshift=30,
        showarrow=False,
        font=dict(
            size=14,
        ),
        align="left",
    )

    fig.update_layout(
        width=800, height=800*0.618,
        plot_bgcolor="white",
        yaxis=dict(
            gridcolor=light_gray,
            title_text="Sales & Profit",
        ),
        xaxis=dict(
            title_text=""
        ),
        legend=dict(
            orientation="h",
            title_text="",
            x=0, xref="paper", xanchor="left",
            y=1, yref="paper", yanchor="bottom",
        ),
        title=dict(
            text="<b>Furniture is the least profitable</b>",
            font_size=16,
            x=0, xref="paper", xanchor="left",
            y=1, yref="paper", yanchor="bottom",
            pad=dict(b=70),
        ),
        margin=dict(
            b=5, t=100,
        )
    )

    return fig


@st.cache_data
def get_figure_for_subcategory():
    df24_wk28 = load_data()
    df24_wk28_profit = df24_wk28.loc[:, ["Category", "Sub-Category", "Profit"]].groupby(
        by=["Category", "Sub-Category"],
    ).sum()

    for cat in df24_wk28_profit.index.get_level_values(0).unique():
        df24_wk28_profit.loc[cat, "Total_Profit_by_Category"] = df24_wk28_profit.loc[cat, "Profit"].sum() # type: ignore

    df24_wk28_profit_by_category = df24_wk28_profit.sort_values(by=["Total_Profit_by_Category", "Profit"]).reset_index()
    fig = go.Figure(go.Bar(
        x=[df24_wk28_profit_by_category["Category"], df24_wk28_profit_by_category["Sub-Category"]],
        y=df24_wk28_profit_by_category["Profit"],
        marker=dict(
            color=[negative_color if profit<0 else positive_color for profit in df24_wk28_profit_by_category["Profit"]],
        )
    ))

    fig.update_traces(
        hovertemplate="%{x}:<br><b>%{y:$,.0f}<b><extra></extra>",
        hoverlabel=dict(
            bgcolor="white",
        )
    )

    fig.add_annotation(
        text="Click the bar to select the sub-category and find out when and where has the most or least profit.",
        x=0, xref="paper", xanchor="left",
        y=1, yref="paper", yanchor="bottom",
        showarrow=False,
        yshift=20, xshift=-20,
        font_size=14,
    )

    fig.update_layout(
        width=800, height=800*0.618,
        plot_bgcolor="white",
        yaxis=dict(
            gridcolor=light_gray,
            title_text="Profit",
            range=[-21000, 61000],
            zeroline=True,
            zerolinecolor=light_gray,
            zerolinewidth=1,
        ),
        title=dict(
            text="<b>The profit of Furniture deteriorates due to the largest loss in Tables</b>",
            font_size=16,
        ),
        margin=dict(b=110)
    )

    return fig

@st.cache_data
def get_figure_for_profit_per_year(sub_category):
    df24_wk28 = load_data()
    if sub_category != "all sub-category": 
        df24_wk28_by_sub_category = df24_wk28.query(
            "`Sub-Category`==@sub_category").loc[:, ["Order Date", "Sales", "Profit"]].set_index(
                "Order Date"
            ).resample("YS").sum()
    else:
        df24_wk28_by_sub_category = df24_wk28.loc[:, ["Order Date", "Sales", "Profit"]].set_index(
                "Order Date"
            ).resample("YS").sum()
        
    fig = px.bar(
        df24_wk28_by_sub_category.reset_index(),
        x="Order Date",
        y="Profit",
        custom_data="Sales",
    )

    fig.update_traces(
        meta=[sub_category],
        marker=dict(
            color=[negative_color if y<0 else positive_color for y in fig.data[0].y] # type: ignore
        ),
        hovertemplate="%{meta[0]} in %{x}<br>Sales: <b>%{customdata[0]:$,.0f}</b><br>Profit: <b>%{y}</b>",
        hoverlabel=dict(bgcolor="white"),
    )

    fig.update_layout(
        width=800, height=800*0.618,
        plot_bgcolor="white",
        xaxis=dict(
            tickformat="%Y",
            nticks=4,
            title_text="Order Year",
        ),
        yaxis=dict(
            gridcolor=light_gray,
            title_text="Profit",
            tickformat="$,.0f",
            zeroline=True,
            zerolinecolor=light_gray,
            zerolinewidth=1,
        ),
        title=dict(
            text=f"<b>The profit of {sub_category} per order year</b>",
            font_size=16,
        )
    )

    return fig

@st.cache_data
def get_figure_for_profit_per_state(sub_category):
    df24_wk28 = load_data()
    if sub_category != "all sub-category":
        df24_wk28_by_subcategory_per_district = df24_wk28.query(
            "`Sub-Category`==@sub_category").loc[:, ["State/Province", "Sales", "Profit"]].groupby(
                by="State/Province"
            ).sum().reset_index().merge(pd.read_csv(assets.US_STATE), on="State/Province", how="inner")
    else:
        df24_wk28_by_subcategory_per_district = df24_wk28.loc[:, ["State/Province", "Sales", "Profit"]].groupby(
                by="State/Province"
            ).sum().reset_index().merge(pd.read_csv(assets.US_STATE), on="State/Province", how="inner")
        
    profits = df24_wk28_by_subcategory_per_district["Profit"]
    colorscale = "RdBu" if (profits < 0).sum() > 0 else "Blues"
    zmax = profits.max() if (profits<0).sum()==0 else max([profits.max(), -profits.min()])
    zmin = profits.min() if (profits<0).sum()==0 else -max([profits.max(), -profits.min()])
    # colorscale = "YlGnBu"

    fig = go.Figure(data=go.Choropleth(
        locations=df24_wk28_by_subcategory_per_district["Code"],
        z=df24_wk28_by_subcategory_per_district["Profit"],
        locationmode="USA-states",
        colorscale=colorscale,
        colorbar_len=0.75,
        customdata=df24_wk28_by_subcategory_per_district.loc[:, ["State/Province", "Sales"]],
        meta=[sub_category],
        hovertemplate="%{meta[0]} in %{customdata[0]}<br>Sales: <b>%{customdata[1]:$,.0f}</b><br>Profit: <b>%{z:$,.0f}</b><extra></extra>",
        hoverlabel=dict(bgcolor="white"),
        zmax=zmax, zmin=zmin, zmid=0, 
    ))

    fig.update_layout(
        width=800, height=800*0.618,
        geo_scope="usa",
        margin=dict(
            l=10, r=10, b=10,
        ),
        title=dict(
            text=f"<b>The profit of {sub_category} per state</b>",
            font_size=16,
        ),
        coloraxis=dict(
            cmid=0,
        )
    )

    return fig

st.header("When and where has the most/least profit?")

st.markdown(
    "Furniture has the least profit, while technology has the most profit. "
    "Do you want to know when and where gives the most/least profit? "
)

col1, _, col2 = st.columns([6, 1, 12])

with col1:
    st.plotly_chart(get_figure_for_category(), use_container_width=True,)

with col2:
    event = st.plotly_chart(
        get_figure_for_subcategory(), 
        use_container_width=True,
        on_select="rerun", selection_mode="points"
    )
try:
    sub_category = event["selection"]["points"][0]["x"][1] # type: ignore
except IndexError:
    sub_category = "all sub-category"


st.divider()
st.markdown(
    f"#### Which year or which state gives the most/least profit for {sub_category}?"
)

col3, _, col4 = st.columns([6, 1, 12])
with col3:
    st.plotly_chart(get_figure_for_profit_per_year(sub_category), use_container_width=True)

with col4:
    st.plotly_chart(get_figure_for_profit_per_state(sub_category), use_container_width=True)