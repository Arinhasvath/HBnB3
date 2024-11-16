from app import create_app
from collections.abc import Mapping

app = create_app()

if __name__ == "__main__":
    app.run()
