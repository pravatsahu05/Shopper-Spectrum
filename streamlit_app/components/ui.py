from pathlib import Path

import streamlit as st

from config import ASSET_DIR


CHART_TEMPLATE = "plotly_dark"
CHART_COLORS = {
    "background": "rgba(7, 17, 31, 0)",
    "paper": "rgba(16, 28, 46, 0.86)",
    "grid": "rgba(148, 163, 184, 0.18)",
    "text": "#e5eefb",
    "muted": "#9fb0c8",
    "blue": "#38bdf8",
    "teal": "#2dd4bf",
    "green": "#34d399",
}


def style_chart(fig):
    fig.update_layout(
        template=CHART_TEMPLATE,
        paper_bgcolor=CHART_COLORS["background"],
        plot_bgcolor=CHART_COLORS["paper"],
        font_color=CHART_COLORS["text"],
        title_font_color=CHART_COLORS["text"],
        margin=dict(l=20, r=20, t=64, b=34),
        coloraxis_colorbar=dict(
            title_font_color=CHART_COLORS["muted"],
            tickfont_color=CHART_COLORS["muted"],
        ),
    )
    fig.update_xaxes(
        gridcolor=CHART_COLORS["grid"],
        zerolinecolor=CHART_COLORS["grid"],
        tickfont_color=CHART_COLORS["muted"],
        title_font_color=CHART_COLORS["muted"],
    )
    fig.update_yaxes(
        gridcolor=CHART_COLORS["grid"],
        zerolinecolor=CHART_COLORS["grid"],
        tickfont_color=CHART_COLORS["muted"],
        title_font_color=CHART_COLORS["muted"],
    )
    return fig


def load_css():
    css_path = Path(ASSET_DIR) / "style.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def page_header(title, subtitle, eyebrow="Shopper Spectrum", pills=None):
    pills = pills or []
    pill_html = "".join(f"<span class='pill'>{pill}</span>" for pill in pills)
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p class="subtitle">{subtitle}</p>
            <div class="pill-row">{pill_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(title, body, tone="insight"):
    class_name = {
        "risk": "risk-card",
        "action": "action-card",
        "recommendation": "recommendation-card",
    }.get(tone, "insight-card")
    st.markdown(
        f"""
        <div class="{class_name}">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(title, body):
    st.markdown(
        f"""
        <div class="section-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(label, value, note=None):
    note_html = f"<p class='muted'>{note}</p>" if note else ""
    st.markdown(
        f"""
        <div class="section-card">
            <div class="small-label">{label}</div>
            <div class="big-number">{value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def timeline(steps):
    items = "".join(
        f"<div class='timeline-step'><span>{index:02d}</span>{step}</div>"
        for index, step in enumerate(steps, start=1)
    )
    st.markdown(f"<div class='timeline'>{items}</div>", unsafe_allow_html=True)
