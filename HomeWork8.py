from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# Вставьте сюда свой OAuth-токен Яндекс Диска
YANDEX_TOKEN = ""
UPLOAD_DIR = "files"

# Получение списка файлов с Яндекс Диска
def get_all_files_from_yandex_disk(path="/"):
    uploaded_files = set()
    offset = 0
    limit = 100

    while True:
        params = urlencode({
            "path": path,
            "limit": limit,
            "offset": offset
        })

        req = Request(
            f"https://cloud-api.yandex.net/v1/disk/resources?{params}",
            headers={"Authorization": f"OAuth {YANDEX_TOKEN}"}
        )

        with urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

        items = data["_embedded"]["items"]

        if not items:
            break

        for item in items:
            uploaded_files.add(item["name"])

        offset += limit

    return uploaded_files

# Генерация HTML страницы

def render_html(local_files, uploaded_files):
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Сервер файлов</title>
        <style>
            li.uploaded {
                background-color: rgba(0, 200, 0, 0.25);
            }
        </style>
    </head>
    <body>
        <h1>Список файлов</h1>
        <ul>
    """

    for file in local_files:
        css_class = "uploaded" if file in uploaded_files else ""
        html += f'<li class="{css_class}">{file}</li>'

    html += """
        </ul>
    </body>
    </html>
    """
    return html


# Обработчик HTTP-запросов

class RequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    # Отправка HTML
    def _send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    # GET-запросы
    def do_GET(self):
        if self.path == "/":
            try:
                if not os.path.exists(UPLOAD_DIR):
                    os.mkdir(UPLOAD_DIR)

                local_files = os.listdir(UPLOAD_DIR)
                uploaded_files = get_all_files_from_yandex_disk("/")

                html = render_html(local_files, uploaded_files)
                self._send_html(html)

            except Exception as e:
                error_html = f"""
                <html>
                <body>
                    <h2>Ошибка</h2>
                    <pre>{str(e)}</pre>
                </body>
                </html>
                """
                self._send_html(error_html)

        elif self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()

        else:
            self.send_error(404)

# Запуск сервера

def run():
    server = HTTPServer(("localhost", 8080), RequestHandler)
    print("Сервер запущен на http://localhost:8080")
    server.serve_forever()

if __name__ == "__main__":
    run()
