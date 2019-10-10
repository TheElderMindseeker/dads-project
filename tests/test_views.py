import pytest

from livebook import create_app
from livebook.models import db


@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

        yield client

        with app.app_context():
            db.drop_all()


def test_hello(client):
    """Test hello view"""
    response = client.get('/')
    assert response.status_code == 200
