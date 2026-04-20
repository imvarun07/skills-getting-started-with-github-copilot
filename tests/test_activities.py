import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_success(self, client, test_activities):
        """Test successfully retrieving all activities"""
        # Arrange
        expected_activities = test_activities

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(expected_activities)
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_activities_have_correct_structure(self, client):
        """Test that activities have the expected structure"""
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity in data.items():
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity
            assert isinstance(activity["participants"], list)

    def test_participant_count_accuracy(self, client, test_activities):
        """Test that participant counts are accurate"""
        # Arrange
        expected_chess_participants = test_activities["Chess Club"]["participants"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert len(data["Chess Club"]["participants"]) == len(expected_chess_participants)
        assert data["Chess Club"]["participants"] == expected_chess_participants
