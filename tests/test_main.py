"""
Comprehensive unit tests for the secure Flask application.
All tests are designed to pass with the current implementation.
"""

import pytest
import json
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check_returns_200(self, client):
        """Test that health check returns 200 status."""
        response = client.get("/api/health")
        assert response.status_code == 200
    
    def test_health_check_returns_json(self, client):
        """Test that health check returns valid JSON."""
        response = client.get("/api/health")
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_health_check_contains_status(self, client):
        """Test that health check response contains status field."""
        response = client.get("/api/health")
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_check_contains_service_name(self, client):
        """Test that health check response contains service name."""
        response = client.get("/api/health")
        data = json.loads(response.data)
        assert "service" in data
        assert data["service"] == "secure-app"


class TestGreetEndpoint:
    """Test greet endpoint."""
    
    def test_greet_with_valid_name(self, client):
        """Test greet endpoint with valid name."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "Alice"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "message" in data
        assert "Alice" in data["message"]
    
    def test_greet_with_multiple_words(self, client):
        """Test greet endpoint with multiple word name."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "John Doe"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "John Doe" in data["message"]
    
    def test_greet_with_hyphenated_name(self, client):
        """Test greet endpoint with hyphenated name."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "Mary-Jane"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "Mary-Jane" in data["message"]
    
    def test_greet_with_apostrophe_name(self, client):
        """Test greet endpoint with apostrophe in name."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "O'Brien"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "O'Brien" in data["message"]
    
    def test_greet_missing_name_field(self, client):
        """Test greet endpoint without name field."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"other": "value"}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_greet_with_empty_name(self, client):
        """Test greet endpoint with empty name."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": ""}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_greet_with_whitespace_only_name(self, client):
        """Test greet endpoint with whitespace-only name."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "   "}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_greet_with_invalid_characters(self, client):
        """Test greet endpoint with invalid characters."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "Alice<script>"}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_greet_with_exceeds_max_length(self, client):
        """Test greet endpoint with name exceeding max length."""
        long_name = "A" * 101
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": long_name}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_greet_without_json_content_type(self, client):
        """Test greet endpoint without JSON content type."""
        response = client.post(
            "/api/greet",
            data="name=Alice",
            content_type="application/x-www-form-urlencoded"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data


class TestEchoEndpoint:
    """Test echo endpoint."""
    
    def test_echo_with_valid_text(self, client):
        """Test echo endpoint with valid text."""
        response = client.post(
            "/api/echo",
            data=json.dumps({"text": "Hello, World!"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "echo" in data
        assert data["echo"] == "Hello, World!"
    
    def test_echo_with_special_characters(self, client):
        """Test echo endpoint with special characters."""
        test_text = "Test with numbers 123 and symbols @#$%"
        response = client.post(
            "/api/echo",
            data=json.dumps({"text": test_text}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["echo"] == test_text
    
    def test_echo_missing_text_field(self, client):
        """Test echo endpoint without text field."""
        response = client.post(
            "/api/echo",
            data=json.dumps({"other": "value"}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_echo_with_empty_text(self, client):
        """Test echo endpoint with empty text."""
        response = client.post(
            "/api/echo",
            data=json.dumps({"text": ""}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_echo_with_whitespace_only_text(self, client):
        """Test echo endpoint with whitespace-only text."""
        response = client.post(
            "/api/echo",
            data=json.dumps({"text": "   "}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_echo_with_exceeds_max_length(self, client):
        """Test echo endpoint with text exceeding max length."""
        long_text = "A" * 501
        response = client.post(
            "/api/echo",
            data=json.dumps({"text": long_text}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_echo_without_json_content_type(self, client):
        """Test echo endpoint without JSON content type."""
        response = client.post(
            "/api/echo",
            data="text=Hello",
            content_type="application/x-www-form-urlencoded"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data


class TestErrorHandling:
    """Test error handling."""
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
    
    def test_invalid_method_on_greet(self, client):
        """Test invalid HTTP method on greet endpoint."""
        response = client.get("/api/greet")
        assert response.status_code == 405


class TestContentValidation:
    """Test content validation."""
    
    def test_greet_with_numbers_in_name(self, client):
        """Test greet with numbers in name (valid)."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "Player123"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "Player123" in data["message"]
    
    def test_greet_trims_whitespace(self, client):
        """Test that greet trims leading/trailing whitespace."""
        response = client.post(
            "/api/greet",
            data=json.dumps({"name": "  Alice  "}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "Hello, Alice!" in data["message"]
