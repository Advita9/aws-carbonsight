from datetime import datetime, timedelta
from statistics import mean

def compute_forecast(history):
    """
    history: list of dict entries like:
    {
        "timestamp": "...",
        "energy_kwh": 0.00023,
        "co2_kg": 0.00008
    }
    """

    if not history:
        return {
            "avg_kwh": 0,
            "avg_co2": 0,
            "forecast_kwh": 0,
            "forecast_co2": 0,
            "prompts_per_day": 0
        }

    # Compute averages
    kwh_values = [h["energy_kwh"] for h in history]
    co2_values = [h["co2_kg"] for h in history]

    avg_kwh = mean(kwh_values)
    avg_co2 = mean(co2_values)

    # Prompts/day
    timestamps = [datetime.fromisoformat(h["timestamp"]) for h in history]
    days = (max(timestamps) - min(timestamps)).days + 1
    prompts_per_day = len(history) / days

    # 7-day forecast
    forecast_kwh = avg_kwh * prompts_per_day * 7
    forecast_co2 = avg_co2 * prompts_per_day * 7

    return {
        "avg_kwh": avg_kwh,
        "avg_co2": avg_co2,
        "forecast_kwh": forecast_kwh,
        "forecast_co2": forecast_co2,
        "prompts_per_day": prompts_per_day
    }
