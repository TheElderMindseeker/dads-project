"""Launch script for the application"""
from livebook import create_app

app = create_app()  # pylint: disable=invalid-name

if __name__ == '__main__':
    app.run('0.0.0.0', 7507)
