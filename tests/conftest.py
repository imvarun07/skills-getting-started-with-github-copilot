import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_activities():
    """Fixture providing fresh test data for each test"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 3,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 2,
            "participants": ["emma@mergington.edu"]
        }
    }


@pytest.fixture
def client(test_activities):
    """Fixture providing a TestClient with fresh test data"""
    # Replace activities with test data
    activities.clear()
    activities.update(test_activities)
    return TestClient(app)
