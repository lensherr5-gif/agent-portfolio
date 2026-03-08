import unittest
from pathlib import Path

from agents.supervisor import Supervisor


class TestMultiAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.permissions_path = str(Path("src/policies/permissions.yaml"))

    def test_normal_collaboration(self):
        s = Supervisor(self.permissions_path)
        result = s.run("compile weekly trend")
        self.assertEqual(result["status"], "succeeded")

    def test_unauthorized_block(self):
        s = Supervisor(self.permissions_path)
        result = s.run("dangerous action", action="delete")
        self.assertEqual(result["status"], "blocked")

    def test_failure_degrades(self):
        s = Supervisor(self.permissions_path)
        result = s.run("unstable task", force_fail=True)
        self.assertEqual(result["status"], "degraded")


if __name__ == "__main__":
    unittest.main()
