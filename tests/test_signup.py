import pytest


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successfully signing up for an activity"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that participant is actually added to the activity"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        activities_response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signing up for a non-existent activity"""
        # Arrange
        email = "student@mergington.edu"
        activity = "Nonexistent Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student(self, client):
        """Test that a student cannot sign up twice for the same activity"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_different_students_same_activity(self, client):
        """Test multiple students can sign up for the same activity"""
        # Arrange
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        activity = "Chess Club"

        # Act
        response1 = client.post(f"/activities/{activity}/signup?email={email1}")
        response2 = client.post(f"/activities/{activity}/signup?email={email2}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity]["participants"]
        assert email1 in participants
        assert email2 in participants
