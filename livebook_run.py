"""Launch script for the application"""
from livebook import create_app

if __name__ == '__main__':
    app = create_app()  # pylint: disable=invalid-name
    app.run('0.0.0.0', 7507)
