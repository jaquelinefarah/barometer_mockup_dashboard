# components/periods_sidebar.py
from __future__ import annotations

import pandas as pd
import streamlit as st
from .periods import PERIOD_PRESETS, get_period_by_preset, previous_period_by_preset


def render_period_sidebar(
    df: pd.DataFrame,
    date_col: str = "date",
    sections: list[str] | None = None,
    show_filters_title: bool = True,   # <- controla o "Filters"
):
    if sections is None:
        sections = ["Company View", "Short Interest"]

    # Header "Filters" (pode desativar no main se quiser)
    if show_filters_title:
        st.sidebar.title("")

    # Controls
    section = st.sidebar.selectbox("Section", sections, index=0)
    preset = st.sidebar.selectbox("Reference period", PERIOD_PRESETS, index=0)

    # Current period
    start_date, end_date = get_period_by_preset(preset)

    # Data filtering
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    cur_df = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)].copy()

    # Previous equivalent period
    prev_start, prev_end = previous_period_by_preset(preset, start_date, end_date)
    prev_df = df[(df[date_col] >= prev_start) & (df[date_col] <= prev_end)].copy()

    period_label = f"{start_date:%Y/%m/%d} – {end_date:%Y/%m/%d}"
    return section, preset, start_date, end_date, cur_df, prev_df, period_label
