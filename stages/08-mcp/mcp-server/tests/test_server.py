import tempfile
import unittest
from pathlib import Path

from mcp_server.server import AuthError, ParamError, TodoMCPServer


class TestMCPServer(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        db_path = str(Path(self.tmp.name) / "todo.db")
        self.server = TodoMCPServer(db_path=db_path, token="secret-token")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_normal_flow(self):
        task = self.server.add_task(token="secret-token", caller="agent", text="write report")
        self.assertEqual(task["done"], False)
        done = self.server.done_task(token="secret-token", caller="agent", task_id=task["id"])
        self.assertEqual(done["done"], True)

    def test_auth_failed(self):
        with self.assertRaises(AuthError):
            self.server.list_tasks(token="wrong", caller="agent")

    def test_invalid_param(self):
        with self.assertRaises(ParamError):
            self.server.add_task(token="secret-token", caller="agent", text="  ")


if __name__ == "__main__":
    unittest.main()
