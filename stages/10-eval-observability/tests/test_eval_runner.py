import unittest

from scripts.run_eval import evaluate


class TestEvalRunner(unittest.TestCase):
    def test_metrics_shape(self):
        metrics = evaluate("evals")
        self.assertIn("success_rate", metrics)
        self.assertIn("failure_counts", metrics)
        self.assertGreater(metrics["total"], 0)


if __name__ == "__main__":
    unittest.main()
