import os
from flask import Flask
import router

app = Flask(__name__)
app.register_blueprint(router.router)


if __name__ == "__main__":
    port = int(os.environ["PORT"])
    app.run(host="0.0.0.0", port=port)