# CC0 1.0 Universal — Public Domain Dedication
import unittest
from genshin_philosophy_protocol import GenshinProtocol, Option


class TestProtocol(unittest.TestCase):
    def setUp(self):
        self.gp = GenshinProtocol(required_stakeholders=["users", "nature"])

    def test_harmony_beats_profit(self):
        a = Option("profit", {"users": 0.3, "nature": -0.5}, centralization=0.9, profit=1.0)
        b = Option("harmony", {"users": 0.5, "nature": 0.2}, centralization=0.1, profit=0.3)
        self.assertEqual(self.gp.judge([a, b]).chosen, "harmony")

    def test_shadow_must_not_be_excluded(self):
        o = Option("blind", {"users": 0.9}, profit=1.0)  # nature unknown
        j = self.gp.judge([o])
        self.assertIsNone(j.chosen)
        self.assertTrue(j.escalate_to_human)

    def test_monopoly_rejected(self):
        o = Option("mono", {"users": 0.5, "nature": 0.5}, centralization=0.95)
        self.assertIn("mono", self.gp.judge([o]).vetoed)

    def test_escalate_when_no_harmony(self):
        o = Option("zero_sum", {"users": 0.8, "nature": -0.8})
        self.assertTrue(self.gp.judge([o]).escalate_to_human)

    def test_replacement_penalized(self):
        a = Option("replace", {"users": 0.5, "nature": 0.5}, replaces_human=True)
        b = Option("partner", {"users": 0.5, "nature": 0.5})
        self.assertEqual(self.gp.judge([a, b]).chosen, "partner")


if __name__ == "__main__":
    unittest.main()
