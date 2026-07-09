class WellnessEngine:
    
    PHASE_DATA = {
        "menstrual": {
            "diet_focus": "Replenishing nutrients, anti-inflammatory meals, and deep hydration.",
            "activity_level": "Low intensity, focusing on flexibility and gentle mobility.",
            "wellness_focus": "Restoration, structural sleep support, and stress minimization."
        },
        "follicular": {
            "diet_focus": "Light proteins, fresh complex carbohydrates, and gut-health support.",
            "activity_level": "Moderate intensity, developing strength and aerobic endurance.",
            "wellness_focus": "Cognitive focus, strategic planning, and social activity."
        },
        "ovulatory": {
            "diet_focus": "Antioxidant-dense foods, fiber integration, and clean energy fuels.",
            "activity_level": "Peak intensity, metabolic conditioning, and high-energy training.",
            "wellness_focus": "High communication, peak confidence, and community collaboration."
        },
        "luteal": {
            "diet_focus": "Magnesium-rich selections, sustained energy sources, and craving control.",
            "activity_level": "Moderate to low intensity, steady-state training, and resistance work.",
            "wellness_focus": "Internal reflection, organization, and gradual recovery planning."
        }
    }

    @classmethod
    def get_recommendations(cls, day_in_cycle: int) -> dict:
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