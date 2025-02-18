import unittest
from unittest.mock import MagicMock, patch

from numpy.f2py.auxfuncs import throw_error

from backend.local_processing.main.main_program import *


class TestMainLoop(unittest.TestCase):

    def setUp(self):
        self.mock_session = MagicMock()
        self.mock_session.commit = MagicMock()
        self.mock_session.close = MagicMock()
        self.mock_wait_until_time_is_up = MagicMock()

        self.mock_camera_full = CurrentCamera(
            camera_id=1,
            snapshot="http://example.com/image.png",
            last_update=datetime.now(),
            cam_status="Online",
            temp_storage_path=".",
            conditions=0
        )

        self.mock_camera_no_snapshot = CurrentCamera(
            camera_id=2,
            snapshot=None,
            last_update=datetime.now(),
            cam_status="Online",
            temp_storage_path=".",
            conditions=0
        )

    #normal operation
    def test_wait_until_time_is_up_normal(self):
        start_time = time.time()
        wait_until_time_is_up(start_time)
        self.assertGreaterEqual(time.time() - start_time, 10)

    # somehow the future
    def test_wait_until_time_is_up_future(self):
        start_time = time.time() + 10
        wait_until_time_is_up(start_time)
        self.assertGreaterEqual(time.time() - start_time, 10)

    # somehow the past
    def test_wait_until_time_is_up_past(self):
        start_time = time.time() - 10
        wait_until_time_is_up(start_time)
        self.assertGreaterEqual(time.time() - start_time, 10)

# what goes in (requires): session, camera, False, start_time, False, None
# what occurs: update camera.lastupdate, update camera.cam_status, log main loop skipping wait
# what goes out (ensures): session.commit(), session.close(), don't wait on time
#(self.mock_session, temp_camera, False, start_time, False, None) passed when Snapshot is missing
    @patch("backend.local_processing.main.main_program.wait_until_time_is_up")
    def test_pass_to_next_loop_SNAPSHOTMISSING(self, mock_wait):
        start_time = datetime.now()
        temp_camera = CurrentCamera(
            camera_id=1,
            snapshot="http://example.com/image.png",
            last_update=start_time,
            cam_status="Online",  # Initial status
            temp_storage_path=".",
            conditions=0
        )
        time.sleep(2)
        with self.assertLogs(None, level="INFO") as log_capture:
            pass_to_next_loop(self.mock_session, temp_camera, False, start_time, False, None)
        self.mock_session.commit.assert_called_once()
        self.mock_session.close.assert_called_once()
        mock_wait.assert_not_called()
        self.assertNotEqual(temp_camera.last_update, start_time)
        self.assertEqual(temp_camera.cam_status, "Offline")
        expected_log = [f'INFO:root:Main Loop skipping wait for Offline camera: {temp_camera.camera_id}']
        self.assertEqual(expected_log, log_capture.output)


    # (self.mock_session, None, False, start_time, False, None) passed when DB is unable to fetch camera info
    @patch("backend.local_processing.main.main_program.wait_until_time_is_up")
    def test_pass_to_next_loop_DBERROR(self, mock_wait):
        start_time = datetime.now()
        with self.assertLogs(None, level="INFO") as log_capture:
            pass_to_next_loop(self.mock_session, None, False, start_time, False, None)
        self.mock_session.commit.assert_called_once()
        self.mock_session.close.assert_called_once()
        mock_wait.assert_not_called()
        expected_log = ['INFO:root:Main Loop Error in Querying Database']
        self.assertEqual(expected_log, log_capture.output)


    # (session, camera, True, start_time, True, None) passed when loop does not fail
    @patch("backend.local_processing.main.main_program.wait_until_time_is_up")
    def test_pass_to_next_loop_SUCCESS(self, mock_wait):
        start_time = datetime.now()
        temp_camera = CurrentCamera(
            camera_id=1,
            snapshot="http://example.com/image.png",
            last_update=start_time,
            cam_status="Online",  # Initial status
            temp_storage_path=".",
            conditions=0
        )
        time.sleep(1)
        with self.assertLogs(None, level="INFO") as log_capture:
            pass_to_next_loop(self.mock_session, temp_camera, True, start_time, True, None)
        self.mock_session.commit.assert_called_once()
        self.mock_session.close.assert_called_once()
        mock_wait.assert_called_once()
        self.assertNotEqual(temp_camera.last_update, start_time)
        self.assertEqual(temp_camera.cam_status, "Online")
        expected_log = [f'INFO:root:Main Loop entering wait for camera: {temp_camera.camera_id}']
        self.assertEqual(expected_log, log_capture.output)


    # (session, camera, True, start_time, False, Error) passed when fails in some other way
    @patch("backend.local_processing.main.main_program.wait_until_time_is_up")
    def test_pass_to_next_loop_OTHERERROR(self, mock_wait):
        start_time = datetime.now()
        temp_camera = CurrentCamera(
            camera_id=1,
            snapshot="http://example.com/image.png",
            last_update=start_time,
            cam_status="Online",  # Initial status
            temp_storage_path=".",
            conditions=0
        )
        time.sleep(1)
        error = 'TestError'
        with self.assertLogs(None, level="INFO") as log_capture:
            pass_to_next_loop(self.mock_session, temp_camera, True, start_time, False, error)
        self.mock_session.commit.assert_called_once()
        self.mock_session.close.assert_called_once()
        mock_wait.assert_called_once()
        self.assertNotEqual(temp_camera.last_update, start_time)
        self.assertEqual(temp_camera.cam_status, "Online")
        expected_log = [f'INFO:root:Main Loop entering wait for camera: {temp_camera.camera_id} with error: {error}']
        self.assertEqual(expected_log, log_capture.output)



    # what goes in (requires): DBSession
    # what occurs: Error, BoolContinue-> True
    # what goes out (ensures): True, DBSession, None
    def test_request_latest_cam_from_db_DBERROR(self):
        self.mock_session.query().order_by().first.return_value = None
        bool_continue, db_session, camera = request_latest_cam_from_db(self.mock_session)
        self.assertTrue(bool_continue)
        self.assertIsNone(camera)
        self.assertIs(db_session, self.mock_session)

    # what goes in (requires): DBSession
    # what occurs: No Snapshot, Bool Continue -> True
    # what goes out (ensures): True, Session, Camera
    def test_request_latest_cam_from_db_NOSNAPSHOT(self):
        self.mock_session.query().order_by().first.return_value = self.mock_camera_no_snapshot
        bool_continue, db_session, camera = request_latest_cam_from_db(self.mock_session)
        self.assertTrue(bool_continue)
        self.assertIs(camera, self.mock_camera_no_snapshot)
        self.assertIs(db_session, self.mock_session)

    # what goes in (requires): DBSession
    # what occurs: Success
    # what goes out (ensures): False, DB_Session, Camera
    def test_request_latest_cam_from_db_SUCCESS(self):
        self.mock_session.query().order_by().first.return_value = self.mock_camera_full
        bool_continue, db_session, camera = request_latest_cam_from_db(self.mock_session)
        self.assertFalse(bool_continue)
        self.assertIs(camera, self.mock_camera_full)
        self.assertIs(db_session, self.mock_session)

    #(camera.snapshot,camera.temp_storage) passed always, returns False,None on success
    @patch("urllib.request.urlretrieve")
    def test_retrieve_image_from_url_into_storage_SUCCESS(self, mock_urlretrieve):
        bool_continue, error = retrieve_image_from_url_into_storage("example", ".")
        self.assertFalse(bool_continue)
        self.assertIsNone(error)
        mock_urlretrieve.assert_called_once()

    @patch("urllib.request.urlretrieve", side_effect=Exception("Test - Error"))
    def test_retrieve_image_from_url_into_storage_FAILURE(self, mock_urlretrieve):
        bool_continue, error = retrieve_image_from_url_into_storage("example", ".")
        self.assertTrue(bool_continue)
        self.assertIsInstance(error, Exception)
        mock_urlretrieve.assert_called_once()

    #pass redundant checks, should receive False, None, integer on success
    @patch("backend.local_processing.main.main_program.process_image", return_value=5)
    @patch("os.path.exists", return_value=True)
    def test_perform_model_evaluation_SUCCESS(self, mock_exists, mock_process_image):
        bool_continue, error, count = perform_model_evaluation(
            False,'/fake/path.png', '/fake/path.pt', 0.5, False, 0, 'fake_image_name'
        )
        mock_exists.assert_called()
        mock_process_image.assert_called_once()
        self.assertFalse(bool_continue)
        self.assertIsNone(error)
        self.assertEqual(count, 5)

    #pass redundant checks, should return True, Error, None on error during model evaluation
    @patch("backend.local_processing.main.main_program.process_image", side_effect=Exception("Test - Error"))
    @patch("os.path.exists", return_value=True)
    def test_perform_model_evaluation_FAILURE(self, mock_exists, mock_process_image):
        bool_continue, error, count = perform_model_evaluation(
            False, '/fake/path.png', '/fake/path.pt', 0.5, False, 0, 'fake_image_name'
        )
        mock_exists.assert_called()
        mock_process_image.assert_called_once()
        self.assertTrue(bool_continue)
        self.assertRaises(Exception, mock_process_image)
        self.assertEqual(count, None)

    #want to ensure that when model_result and camera are passed and no historical value is present
    #that add and commit are still called
    def test_update_traffic_count_HISTORICAL_NONE(self):
        self.mock_session.query().filter().order_by().first.return_value = None
        bool_continue, error, db_session = update_traffic_count(10, self.mock_camera_full, self.mock_session)
        self.assertFalse(bool_continue)
        self.assertIsNone(error)
        self.assertIs(db_session, self.mock_session)
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called()

    #pass camera and count greater than historical maximum,
    #causing historical and specific count and time to be replaced by passed in camera values
    def test_update_traffic_count_HISTORICAL_LESS(self):
        new_time = datetime.now()
        mock_historical = TrafficCount(
            cam_id=1,
            traffic_count=5,
            traffic_time=new_time,
            max_traffic_count=8,
            max_traffic_time=new_time
        )
        #the query REALLY doesn't like mock
        self.mock_session.query().filter().order_by().first.return_value = mock_historical
        model_result = 10
        time.sleep(2)
        bool_continue, error, db_session = update_traffic_count(model_result, self.mock_camera_full, self.mock_session)
        self.assertFalse(bool_continue)
        self.assertIsNone(error)
        self.assertIs(db_session, self.mock_session)
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called()
        #checking the actual TrafficCount object created in update_traffic_count
        added_object = self.mock_session.add.call_args[0][0]
        self.assertEqual(added_object.cam_id, self.mock_camera_full.camera_id)
        self.assertEqual(added_object.traffic_count, model_result)
        self.assertEqual(added_object.max_traffic_count, model_result)
        self.assertNotEqual(added_object.traffic_time, new_time)
        self.assertNotEqual(added_object.max_traffic_time, new_time)


    def test_update_traffic_count_HISTORICAL_MORE(self):
        new_time = datetime.now()
        mock_historical = TrafficCount(
            cam_id=1,
            traffic_count=5,
            traffic_time=new_time,
            max_traffic_count=12,
            max_traffic_time=new_time
        )
        #the query REALLY doesn't like mock
        self.mock_session.query().filter().order_by().first.return_value = mock_historical
        model_result = 8
        time.sleep(2)
        bool_continue, error, db_session = update_traffic_count(model_result, self.mock_camera_full, self.mock_session)
        self.assertFalse(bool_continue)
        self.assertIsNone(error)
        self.assertIs(db_session, self.mock_session)
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called()
        #checking the actual TrafficCount object created in update_traffic_count
        added_object = self.mock_session.add.call_args[0][0]
        self.assertEqual(added_object.cam_id, self.mock_camera_full.camera_id)
        self.assertEqual(added_object.traffic_count, model_result)
        self.assertEqual(added_object.max_traffic_count, mock_historical.max_traffic_count)
        self.assertNotEqual(added_object.traffic_time, new_time)
        self.assertEqual(added_object.max_traffic_time, mock_historical.max_traffic_time)


    def test_update_traffic_count_sqlalchemy_error(self):
        self.mock_session.query().filter().order_by().first.return_value = throw_error
        bool_continue, error, db_session = update_traffic_count(10, self.mock_camera_full, self.mock_session)
        self.assertTrue(bool_continue)
        self.assertIsInstance(error, Exception)
        self.assertEqual(self.mock_session, db_session)


if __name__ == "__main__":
    unittest.main()