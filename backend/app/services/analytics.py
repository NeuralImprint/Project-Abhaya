"""
Project Abhaya — Cycle Analytics Engine
Computes menstrual cycle metrics, predictions, and anomaly alerts.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any


class CycleEngine:
    """Analysis engine for menstrual cycle metrics and health alerts."""

    @staticmethod
    def calculate_metrics(past_cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze cycle history to compute average length, predict next period,
        and flag irregularities.

        Args:
            past_cycles: List of dicts with 'start_date' keys (YYYY-MM-DD format)

        Returns:
            Dict with status, average cycle length, next predicted date, and alerts
        """
        if len(past_cycles) < 2:
            return {"status": "insufficient_data", "alerts": []}

        lengths = []
        for i in range(len(past_cycles) - 1):
            start_current = datetime.strptime(past_cycles[i]["start_date"], "%Y-%m-%d")
            start_next = datetime.strptime(past_cycles[i + 1]["start_date"], "%Y-%m-%d")
            lengths.append((start_next - start_current).days)

        avg_length = sum(lengths) / len(lengths)
        variance = max(lengths) - min(lengths)

        # Generate health alerts based on cycle patterns
        alerts = []
        if variance > 7:
            alerts.append("HIGH_CYCLE_VARIABILITY_DETECTED")
        if avg_length > 35 or avg_length < 21:
            alerts.append("ABNORMAL_CYCLE_DURATION_ALERT")

        # Predict next period based on average cycle length
        latest_start = datetime.strptime(past_cycles[-1]["start_date"], "%Y-%m-%d")
        next_predicted = latest_start + timedelta(days=round(avg_length))

        # Estimate ovulation (typically ~14 days before next period)
        ovulation_predicted = next_predicted - timedelta(days=14)

        # Fertility window (5 days before ovulation + ovulation day)
        fertility_start = ovulation_predicted - timedelta(days=5)
        fertility_end = ovulation_predicted + timedelta(days=1)

        return {
            "status": "success",
            "average_cycle_length": round(avg_length, 1),
            "cycle_variance_days": variance,
            "next_predicted_date": next_predicted.strftime("%Y-%m-%d"),
            "ovulation_predicted_date": ovulation_predicted.strftime("%Y-%m-%d"),
            "fertility_window": {
                "start": fertility_start.strftime("%Y-%m-%d"),
                "end": fertility_end.strftime("%Y-%m-%d")
            },
            "alerts": alerts
        }
