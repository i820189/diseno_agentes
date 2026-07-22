import unittest

from agente.domain import CATALOGO, PESOS, calcular_utilidad


class UtilityRulesTests(unittest.TestCase):
    def test_weights_are_fixed_and_sum_to_one(self):
        self.assertAlmostEqual(sum(PESOS.values()), 1.0)

    def test_matching_preference_improves_utility(self):
        option = CATALOGO[0]
        matching = calcular_utilidad(option, "cumpleaños", ["práctico"])
        neutral = calcular_utilidad(option, "cumpleaños", [])
        self.assertGreater(matching["utility_score"], neutral["utility_score"])

    def test_score_is_bounded(self):
        score = calcular_utilidad(CATALOGO[0], "cumpleaños", ["práctico"])["utility_score"]
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)


if __name__ == "__main__":
    unittest.main()
