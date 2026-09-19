import unittest
from app.models.environmental import EnvironmentalProfile
from app.services.environmental_reasoning import EnvironmentalReasoningEngine

class TestEnvironmentalReasoning(unittest.TestCase):
    def setUp(self):
        self.engine = EnvironmentalReasoningEngine()

    def test_three_variable_rule_satisfied(self):
        profile = EnvironmentalProfile(
            region="semi-arid",
            soil_organic_carbon=0.3,
            annual_rainfall_mm=420.0,
            crop_type="wheat monoculture",
            land_use="agriculture"
        )
        vars_used, interactions, uncertainties = self.engine.analyze_interactions(profile, [])
        is_valid = self.engine.validate_three_variables(vars_used)
        self.assertTrue(is_valid, f"Must pass 3-variable validation (got {len(vars_used)}: {vars_used})")
        self.assertGreaterEqual(len(interactions), 1)

    def test_three_variable_rule_detects_insufficient_data(self):
        sparse_profile = EnvironmentalProfile(
            region="semi-arid"
        )
        vars_used, interactions, uncertainties = self.engine.analyze_interactions(sparse_profile, [])
        is_valid = self.engine.validate_three_variables(vars_used)
        self.assertFalse(is_valid, "Single variable must fail 3-variable validation")
        self.assertGreater(len(uncertainties), 0, "Must output uncertainty statement when constrained")

    def test_pollinator_pesticide_coupling(self):
        profile = EnvironmentalProfile(
            pesticide_usage="frequent / intensive",
            crop_type="wheat monoculture",
            notes="Observed acute pollinator decline"
        )
        vars_used, interactions, uncertainties = self.engine.analyze_interactions(profile, [])
        found_trophic_loop = any("trophic" in i.interaction_type.lower() or "pollinator" in " ".join(i.variables).lower() for i in interactions)
        self.assertTrue(found_trophic_loop, "Must identify pesticide-pollinator trophic vulnerability")

if __name__ == "__main__":
    unittest.main()
