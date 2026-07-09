from datetime import datetime, timedelta
from typing import List, Dict, Any

class CycleEngine:
    """ANALYSIS ENGINE FOR MENSTRUAL CYCLE METRICS AND ALERTS"""

    @staticmethod
    def calculate_metrics(past_cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(past_cycles) < 2:
            return {"status": "insufficient_data", "alerts": []}

        lengths = []
        for i in range(len(past_cycles) - 1):
            start_current = datetime.strptime(past_cycles[i]["start_date"], "%Y-%m-%d")
            start_next = datetime.strptime(past_cycles[i+1]["start_date"], "%Y-%m-%d")
            lengths.append((start_next - start_current).days)

        avg_length = sum(lengths) / len(lengths)
        variance = max(lengths) - min(lengths)
        
        alerts = []
        if variance > 7:
            alerts.append("HIGH_CYCLE_VARIABILITY_DETECTED")
        if avg_length > 35 or avg_length < 21:
            alerts.append("ABNORMAL_CYCLE_DURATION_ALERT")

        latest_start = datetime.strptime(past_cycles[-1]["start_date"], "%Y-%m-%d")
        next_predicted = latest_start + timedelta(days=round(avg_length))

        return {
            "status": "success",
            "average_cycle_length": round(avg_length, 1),
            "next_predicted_date": next_predicted.strftime("%Y-%m-%d"),
            "alerts": alerts
        }