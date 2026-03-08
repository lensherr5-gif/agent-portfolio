import tempfile
import unittest

from agent.react_loop import ReactConfig, ReactLoop


def tool_add(args):
    return args["a"] + args["b"]


class TestReactLoop(unittest.TestCase):
    def test_success_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            planner_steps = iter(
                [
                    {"action": "tool", "tool": "add", "args": {"a": 1, "b": 2}, "thought": "calc"},
                    {"action": "finish", "answer": "3", "thought": "done"},
                ]
            )

            def planner(_state):
                return next(planner_steps)

            loop = ReactLoop({"add": tool_add}, run_dir=tmp)
            result = loop.run("1+2", planner, run_id="ok", config=ReactConfig(max_steps=4))
            self.assertEqual(result["status"], "succeeded")
            self.assertEqual(result["answer"], "3")

    def test_max_steps_termination(self):
        with tempfile.TemporaryDirectory() as tmp:
            def planner(_state):
                return {"action": "tool", "tool": "add", "args": {"a": 1, "b": 1}}

            loop = ReactLoop({"add": tool_add}, run_dir=tmp)
            result = loop.run("loop", planner, run_id="max", config=ReactConfig(max_steps=2))
            self.assertEqual(result["status"], "max_steps_reached")

    def test_tool_failure_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            def boom(_args):
                raise RuntimeError("tool crashed")

            def planner(_state):
                return {"action": "tool", "tool": "boom", "args": {}}

            loop = ReactLoop({"boom": boom}, run_dir=tmp)
            result = loop.run("fail", planner, run_id="fail", config=ReactConfig(max_steps=3, max_failures=1))
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["failure_taxonomy"], "tool_error")


if __name__ == "__main__":
    unittest.main()
