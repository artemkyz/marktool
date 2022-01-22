
"""Application entry point."""
from marktool import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
