from sanic import Sanic
from Routes.routes import bp
from sanic.response import text,json

app = Sanic(__name__)

app.blueprint(bp)

@app.route("/<path:path>")
async def catch_all(request, path):
    return json({"Message":"Invalid route"}, status=404)

if __name__ == '__main__':
    app.run()