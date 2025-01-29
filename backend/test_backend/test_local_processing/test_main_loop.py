import pytest
from unittest.mock import patch, MagicMock, call

from backend.local_processing.main.main_program import *

#testing the timing of the loop
def test_wait_until_time_is_up():
    start_time = time.time()
    end_time = time.time() - start_time
    while end_time <= 10:
        time.sleep(1)
        end_time = time.time() - start_time
    assert(end_time >= 10)

class MockCurrentCamera:
    def __init__(self, camera_id, snapshot, temp_storage_path, last_update):
        self.camera_id = camera_id
        self.snapshot = snapshot
        self.temp_storage_path = temp_storage_path
        self.last_update = last_update
        self.cam_status = "Online"

class MockTrafficCount:
    def __init__(self, cam_id, traffic_count, traffic_time, max_traffic_count, max_traffic_time):
        self.cam_id = cam_id
        self.traffic_count = traffic_count
        self.traffic_time = traffic_time
        self.max_traffic_count = max_traffic_count
        self.max_traffic_time = max_traffic_time

#WILL REQUIRE MOCKING
#requires a session with a database, a camera object, a boolean
#that decribes whether to wait, a starting time for the beginning of the loop,
#, a boolean full_pass that describes whether no exceptions have been raised,
#, and an error that can be None or the exception that was raised
#def test_pass_to_next_loop():
