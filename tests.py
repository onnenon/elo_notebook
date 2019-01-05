import unittest
import elo


class EloTests(unittest.TestCase):
    def test_calc_kill_score(self):
        self.assertEqual(10, elo.calc_kill_score(1))

    def test_calc_down_score(self):
        self.assertEqual(-20, elo.calc_down_score(2))

    def test_calc_place_score(self):
        self.assertEqual(-74, elo.calc_place_score(88))

    def test_calc_assist_score(self):
        self.assertEqual(140, elo.calc_assist_score(7))

    def test_calc_accuracy_score(self):
        self.assertAlmostEqual(.975, elo.calc_accuracy_score(.25))

    def test_calc_loss_mult(self):
        self.assertAlmostEqual(1.08, elo.calc_loss_mult(25, 50))

    def test_calc_time_survived_mult(self):
        self.assertALmostEqual(0.62, elo.calc_time_survived_mult(3, 25))

    def test_calc_scale_bonus(self):
        self.assertAlmostEqual(0.875, elo.calc_scale_bonus(25, 50))

    def test_calc_elo(self):
        self.assertEqual((-85.93, -85.93), elo.calc_elo(-74, -20, 10, 140, .975, 1.08, 0.62, 0.875, False, True, False))


if __name__ == '__main__':
    unittest.main()
