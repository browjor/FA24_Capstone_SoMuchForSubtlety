from backend.database.create_db import Base
from backend.local_processing.main.main_program import *
import unittest
from unittest.mock import patch
from datetime import timedelta


class DatabaseIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize test database
        cls.engine = create_engine(os.getenv('TEST_SQLITE_DB_LOC'))
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
    @classmethod
    def tearDownClass(cls):
        # Drop all tables after tests
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        # Create a new session for each test
        self.session = self.Session()

    def tearDown(self):
        # Rollback any session transactions and close after each test
        self.session.rollback()
        self.session.close()

class TestMainProgramIntegration(DatabaseIntegrationTest):
    def test_main_program_integ_SUCCESS(self):
        # Setup a dummy camera entry
        test_cam = CurrentCamera(
            camera_id=99999,
            cam_status="Online",
            snapshot="http://example.com/image.png",
            latitude=38.27,
            longitude=-85.81,
            last_update=datetime.now() - timedelta(days=1),
            temp_storage_path=".",
            conditions=0,
            zone=1
        )
        self.session.add(test_cam)
        self.session.commit()

        #testing if request_latest_cam actually returns a camera session from the object
        bool_continue, test_session, test_camera = request_latest_cam_from_db(self.session)
        assert not bool_continue
        assert test_camera.camera_id == 99999

        #testing that snapshot and temp_storage_path will be given from camera object
        with patch('urllib.request.urlretrieve') as mock_retrieve:
            mock_retrieve.return_value = ("./current.png", None)
            test_retrieval_result = retrieve_image_from_url_into_storage(test_camera.snapshot, test_camera.temp_storage_path)
            assert not test_retrieval_result[0]

        #testing that camera conditions will be given from camera object (is needed for evaluation mode)
        with patch('backend.local_processing.main.main_program.process_image', return_value=5):
            with patch("os.path.exists", return_value=True):
                test_model_results = perform_model_evaluation(
                    False, '/fake/path.png', '/fake/path.pt', 0.5, True, test_camera.conditions, "image_name"
                )
                assert not test_model_results[0]
                assert test_model_results[2] == 5

        # Update traffic count
        test_update_result = update_traffic_count(test_model_results[2], test_camera, self.session)
        assert not test_update_result[0]

        updated_traffic = self.session.query(TrafficCount).filter_by(cam_id=99999).first()
        assert updated_traffic is not None
        assert updated_traffic.traffic_count == 5




if __name__ == "__main__":
    unittest.main()