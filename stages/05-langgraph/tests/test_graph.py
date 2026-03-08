import unittest

from workflow.graph import WorkflowGraph


class TestWorkflowGraph(unittest.TestCase):
    def test_normal_flow(self):
        graph = WorkflowGraph(checkpoint_dir="tests/.tmp-checkpoints")
        state = graph.run("summarize weather", run_id="normal")
        self.assertEqual(state["status"], "succeeded")

    def test_requires_approval(self):
        graph = WorkflowGraph(checkpoint_dir="tests/.tmp-checkpoints")
        state = graph.run("delete user account", run_id="approval")
        self.assertEqual(state["status"], "awaiting_approval")

        resumed = graph.run("delete user account", run_id="approval", resume=True, approved=True)
        self.assertEqual(resumed["status"], "succeeded")

    def test_failed_path(self):
        graph = WorkflowGraph(checkpoint_dir="tests/.tmp-checkpoints")
        state = graph.run("fail this action", run_id="failed", max_retries=1)
        self.assertEqual(state["status"], "failed")


if __name__ == "__main__":
    unittest.main()
