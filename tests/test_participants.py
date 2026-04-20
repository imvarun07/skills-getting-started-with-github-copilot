import pytest


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_remove_participant_success(self, client):
        """Test successfully removing a participant from an activity"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]

    def test_remove_participant_actually_removed(self, client):
        """Test that participant is actually removed from the activity"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")
        activities_response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities_data = activities_response.json()
        assert email not in activities_data[activity]["participants"]

    def test_remove_participant_activity_not_found(self, client):
        """Test removing participant from non-existent activity"""
        # Arrange
        email = "student@mergington.edu"
        activity = "Nonexistent Club"

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_remove_participant_not_in_activity(self, client):
        """Test removing a participant who is not signed up"""
        # Arrange
        email = "notregistered@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not found in this activity" in data["detail"]

    def test_remove_then_add_same_participant(self, client):
        """Test that a participant can be removed and re-added"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act - Remove
        remove_response = client.delete(f"/activities/{activity}/participants/{email}")
        # Act - Re-add
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert remove_response.status_code == 200
        assert signup_response.status_code == 200
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]
