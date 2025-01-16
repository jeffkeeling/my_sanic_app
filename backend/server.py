from sanic import Sanic
from sanic_cors import CORS
from api.routes import api
from database import init_db

app = Sanic("user_management_app")
CORS(app)

@app.listener('before_server_start')
async def setup_db(app, loop):
    await init_db()

app.blueprint(api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)