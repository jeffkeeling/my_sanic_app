from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

app = Sanic("NextJSBackend")
CORS(app)

@app.route("/api/hello", methods=["GET"],  name="get_hello")
async def hello_world(request):
    return json({"message": "Hello from Sanic!"})

@app.route("/api/data", methods=["POST"],  name="post_data")
async def receive_data(request):
    data = request.json
    # Process the data here
    return json({"status": "success", "received": data})

users = [{"id": 1, "name": "Alice", "email": "test@23.com"}]

@app.route("/api/users2", methods=["GET"],  name="test_users")
async def receive_data(request):
    data = request.json
    # Process the data here
    return json({"status": "success", "received": users})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)