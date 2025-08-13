# components/periods.py
from datetime import datetime, timedelta
from typing import Tuple
import pandas as pd

PERIOD_PRESETS = [
    "Last closed week",
    "Last 4 weeks",
    "Last 3 months",
    "Last 12 months",
]

def _last_closed_week() -> Tuple[pd.Timestamp, pd.Timestamp]:
    """Seg–Sex da última semana fechada, como timestamps."""
    today = datetime.today()
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday + 7)  # volta 1 semana completa
    friday = monday + timedelta(days=4)
    return pd.to_datetime(monday.date()), pd.to_datetime(friday.date())

def _last_n_weeks_range(n: int) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """N semanas completas terminando na última semana fechada (0 + n-1 anteriores)."""
    # semana 0
    start0, end0 = _last_closed_week()
    # volta (n-1) semanas
    startN = start0 - pd.Timedelta(weeks=n-1)
    return startN.normalize(), end0.normalize()

def get_period_by_preset(preset: str) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """Período atual para cada preset (sempre terminando na sex. da última semana fechada)."""
    _, anchor_end = _last_closed_week()

    if preset == "Last closed week":
        return _last_closed_week()

    if preset == "Last 4 weeks":
        return _last_n_weeks_range(4)

    if preset == "Last 3 months":
        start = (anchor_end + pd.Timedelta(days=1)) - pd.DateOffset(months=3)
        return start.normalize(), anchor_end.normalize()

    if preset == "Last 12 months":  # rolling 12 meses
        start = (anchor_end + pd.Timedelta(days=1)) - pd.DateOffset(years=1)
        return start.normalize(), anchor_end.normalize()

    # fallback (não deveria cair aqui)
    return None, anchor_end

def previous_period_by_preset(preset: str,
                              start_date: pd.Timestamp,
                              end_date: pd.Timestamp) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """Janela imediatamente anterior equivalente ao preset atual."""
    start_date = pd.to_datetime(start_date); end_date = pd.to_datetime(end_date)

    if preset == "Last closed week":
        prev_end = start_date - pd.Timedelta(days=1)      # sexta anterior
        prev_start = prev_end - pd.Timedelta(days=4)      # segunda anterior
        return prev_start.normalize(), prev_end.normalize()

    if preset == "Last 4 weeks":
        prev_end = start_date - pd.Timedelta(days=1)
        prev_start = prev_end - pd.Timedelta(weeks=4) + pd.Timedelta(days=1)
        return prev_start.normalize(), prev_end.normalize()

    if preset == "Last 3 months":
        prev_end = start_date - pd.Timedelta(days=1)
        prev_start = (prev_end + pd.Timedelta(days=1)) - pd.DateOffset(months=3)
        return prev_start.normalize(), prev_end.normalize()

    if preset == "Last 12 months":
        prev_end = start_date - pd.Timedelta(days=1)
        prev_start = (prev_end + pd.Timedelta(days=1)) - pd.DateOffset(years=1)
        return prev_start.normalize(), prev_end.normalize()

    # fallback: mesma duração deslocada pra trás
    prev_end = start_date - pd.Timedelta(days=1)
    prev_start = prev_end - (end_date - start_date)
    return prev_start.normalize(), prev_end.normalize()
