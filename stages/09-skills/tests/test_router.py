import unittest

from skills.router import SkillMeta, SkillRouter


class TestSkillRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.router = SkillRouter()
        self.router.register(
            SkillMeta(
                name="job-hunter",
                version="1.0.0",
                risk="medium",
                enabled=True,
                approved_users={"alice"},
                handler=lambda q: f"handled:{q}",
            )
        )

    def test_route_match(self):
        out = self.router.execute("alice", "please parse this JD")
        self.assertTrue(out.startswith("handled:"))

    def test_route_miss(self):
        out = self.router.execute("alice", "tell me weather")
        self.assertEqual(out, "NO_SKILL_MATCH")

    def test_unauthorized_block(self):
        out = self.router.execute("bob", "interview questions for this jd")
        self.assertEqual(out, "SKILL_BLOCKED")


if __name__ == "__main__":
    unittest.main()
