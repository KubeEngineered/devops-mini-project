import http.server
import socketserver

PORT = 8080

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>This is as simple an app as you get to see in tech</h1>")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"Server running on port {PORT}...")
        httpd.serve_forever()
