import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
import time, json, hmac, hashlib
from backend.local_processing.server_endpoint.app import app, verify_hmac, generate_response_hmac, fetch_traffic_data_from_db


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.mock_session = MagicMock()
        self.shared_secret = "test_secret"

    #requires valid hmac, returns True
    @patch("backend.local_processing.server_endpoint.app.SHARED_SECRET", "test_secret")
    def test_verify_hmac_SUCCESS(self):
        timestamp = str(int(time.time()))
        message = timestamp.encode()
        valid_hmac = hmac.new(self.shared_secret.encode(), message, hashlib.sha256).hexdigest()
        mock_request = MagicMock()
        #request is an object with multiple properties evaluated in verify_hmac, so it needs to
        #be different things at different times
        mock_request.headers.get.side_effect = lambda x: valid_hmac if x == "X-HMAC-Signature" else timestamp
        self.assertTrue(verify_hmac(mock_request))

    #when no headers are supplied, returns False
    def test_verify_hmac_NOHEADERS(self):
        mock_request = MagicMock()
        mock_request.headers.get.side_effect = lambda x: None
        self.assertFalse(verify_hmac(mock_request))

    #when bad timestamp is supplied, returns false
    def test_verify_hmac_BADTIMESTAMP(self):
        timestamp = str(int(time.time()) - 400)  # More than 300 seconds old
        mock_request = MagicMock()
        mock_request.headers.get.side_effect = lambda x: timestamp if x == "X-Timestamp" else "test_hmac"
        self.assertFalse(verify_hmac(mock_request))

    #tests that generating response HMAC with same input results in same output
    @patch("backend.local_processing.server_endpoint.app.SHARED_SECRET", "test_secret")
    def test_generate_response_hmac(self):
        response_json = {"data": [{"density": 0.5, "lat": 40.0, "lon": -75.0}], "timestamp": "1234567890"}
        expected_message = json.dumps(response_json, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode()
        expected_hmac = hmac.new(self.shared_secret.encode(), expected_message, hashlib.sha256).hexdigest()

        self.assertEqual(generate_response_hmac(response_json), expected_hmac)

    #tests that a list is returned from fetch_traffic_data
    @patch("backend.local_processing.server_endpoint.app.sessionmaker")
    def test_fetch_traffic_data_from_db(self, mock_sessionmaker):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session

        mock_query = mock_session.return_value.query().filter().order_by().distinct().all()
        mock_query.return_value = []

        self.assertEqual(fetch_traffic_data_from_db(), [])

    #tests latest_traffic_endpoint given correct inner methods
    @patch("backend.local_processing.server_endpoint.app.verify_hmac", return_value=True)
    @patch("backend.local_processing.server_endpoint.app.data_condition.wait", return_value=True)
    @patch("backend.local_processing.server_endpoint.app.traffic_data", new_callable=lambda: [{"density": 0.7, "lat": 40.7128, "lon": -74.0060}])
    def test_latest_traffic_valid(self, mock_traffic, mock_condition, mock_hmac):
        response = self.app.get("/latest-traffic", headers={
            "X-HMAC-Signature": "valid_hmac",
            "X-Timestamp": str(int(time.time()))
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json)

    #tests that when the endpoint is given no headers, it responds with the correct status code (403)
    @patch("backend.local_processing.server_endpoint.app.verify_hmac", return_value=False)
    def test_latest_traffic_unauthorized(self, mock_hmac):
        response = self.app.get("/latest-traffic", headers={})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {"error": "Unauthorized"})


if __name__ == "__main__":
    unittest.main()
