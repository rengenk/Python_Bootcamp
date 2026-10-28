from flask import Flask, render_template
from di.container import Container
from pathlib import Path

def create_app():
    app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "web" / "templates")
    )
    container = Container()
    container.register_routes(app)

    @app.get("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
