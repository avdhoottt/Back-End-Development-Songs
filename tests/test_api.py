import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_update_song(client):
    """Test updating a song"""
    update_data = {
        "name": "Updated Song Name"
    }
    response = client.put(
        '/song/1',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.get_json()['name'] == "Updated Song Name"

def test_delete_song(client):
    """Test deleting a song"""
    # First verify the song exists
    response = client.get('/song/1')
    assert response.status_code == 200

    # Delete the song
    response = client.delete('/song/1')
    assert response.status_code == 204

    # Verify it's gone
    response = client.get('/song/1')
    assert response.status_code == 404
