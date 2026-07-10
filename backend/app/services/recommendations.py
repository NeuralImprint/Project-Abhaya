"""
Project Abhaya — Wellness Recommendations Engine
Phase-based personalized recommendations for diet, activity, and wellness.
"""


class WellnessEngine:
    """Maps menstrual cycle days to biological phases and returns tailored recommendations."""

    PHASE_DATA = {
        "menstrual": {
            "diet_focus": "Replenishing nutrients, anti-inflammatory meals, and deep hydration.",
            "activity_level": "Low intensity, focusing on flexibility and gentle mobility.",
            "wellness_focus": "Restoration, structural sleep support, and stress minimization.",
            "tips": [
                "Increase iron-rich foods (spinach, lentils, dark chocolate)",
                "Stay hydrated — aim for 8-10 glasses of warm water",
                "Try gentle yoga or stretching for cramp relief"
            ]
        },
        "follicular": {
            "diet_focus": "Light proteins, fresh complex carbohydrates, and gut-health support.",
            "activity_level": "Moderate intensity, developing strength and aerobic endurance.",
            "wellness_focus": "Cognitive focus, strategic planning, and social activity.",
            "tips": [
                "Great time to start new projects — energy is rising",
                "Include fermented foods for gut health",
                "Try cardio or dance workouts"
            ]
        },
        "ovulatory": {
            "diet_focus": "Antioxidant-dense foods, fiber integration, and clean energy fuels.",
            "activity_level": "Peak intensity, metabolic conditioning, and high-energy training.",
            "wellness_focus": "High communication, peak confidence, and community collaboration.",
            "tips": [
                "Peak energy — ideal for HIIT and intense workouts",
                "Load up on cruciferous vegetables (broccoli, kale)",
                "Social energy is highest — great for networking"
            ]
        },
        "luteal": {
            "diet_focus": "Magnesium-rich selections, sustained energy sources, and craving control.",
            "activity_level": "Moderate to low intensity, steady-state training, and resistance work.",
            "wellness_focus": "Internal reflection, organization, and gradual recovery planning.",
            "tips": [
                "Manage cravings with dark chocolate and nuts",
                "Prioritize sleep — aim for 7-9 hours",
                "Gentle walks and pilates work well in this phase"
            ]
        }
    }

    @classmethod
    def get_recommendations(cls, day_in_cycle: int) -> dict:
        """
        Return phase-specific recommendations based on the current cycle day.

        Args:
            day_in_cycle: Current day in the menstrual cycle (1-45)

        Returns:
            Dict with phase info and personalized recommendations
        """
        if 1 <= day_in_cycle <= 5:
            phase = "menstrual"
        elif 6 <= day_in_cycle <= 11:
            phase = "follicular"
        elif 12 <= day_in_cycle <= 16:
            phase = "ovulatory"
        else:
            phase = "luteal"

        return {
            "current_cycle_day": day_in_cycle,
            "biological_phase": phase.capitalize(),
            "recommendations": cls.PHASE_DATA[phase]
        }
