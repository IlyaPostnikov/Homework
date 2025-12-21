from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

DATA_FILE = "tasks.txt"


class Task:
    def __init__(self, id_, title, priority, is_done=False):
        self.id = id_
        self.title = title
        self.priority = priority
        self.isDone = is_done

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "isDone": self.isDone
        }


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load()

    def add_task(self, title, priority):
        task = Task(self.next_id, title, priority)
        self.tasks.append(task)
        self.next_id += 1
        self.save()
        return task

    def get_all_tasks(self):
        return [task.to_dict() for task in self.tasks]

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.isDone = True
                self.save()
                return True
        return False

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.get_all_tasks(), f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                task = Task(
                    item["id"],
                    item["title"],
                    item["priority"],
                    item["isDone"]
                )
                self.tasks.append(task)
            if self.tasks:
                self.next_id = max(task.id for task in self.tasks) + 1


manager = TaskManager()


class RequestHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/tasks":
            self._send_json(manager.get_all_tasks())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/tasks":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            title = data.get("title")
            priority = data.get("priority")

            if not title or not priority:
                self.send_error(400, "Invalid data")
                return

            task = manager.add_task(title, priority)
            self._send_json(task.to_dict())

        elif self.path.startswith("/tasks/") and self.path.endswith("/complete"):
            try:
                task_id = int(self.path.split("/")[2])
            except (IndexError, ValueError):
                self.send_error(400)
                return

            if manager.complete_task(task_id):
                self.send_response(200)
                self.end_headers()
            else:
                self.send_error(404)

        else:
            self.send_error(404)


def run():
    server = HTTPServer(("localhost", 8080), RequestHandler)
    print("Server running on http://localhost:8080")
    server.serve_forever()


if __name__ == "__main__":
    run()
