from backend.database.create_db import Base
from backend.local_processing.auxiliary.aux_program import *
import unittest
from unittest.mock import patch
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

class TestAuxIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.engine = create_engine(os.getenv('TEST_SQLITE_DB_LOC'))
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def tearDownClass(self):
        Base.metadata.drop_all(self.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

class TestAuxProgramIntegration(TestAuxIntegration):

    @patch.dict(os.environ, {"SQLite_DB_LOC": os.getenv('TEST_SQLITE_DB_LOC')})
    def test_backup_SUCCESS(self):
        for i in range(1,850):
            self.session.add(TrafficCount(
                cam_id=i,
                traffic_count=5,
                traffic_time=datetime.now() - timedelta(minutes=i),
                max_traffic_count=5,
                max_traffic_time=datetime.now() - timedelta(minutes=i+i)
            ))
        self.session.commit()
        #get first and last in 850 traffic counts
        first_traffic_count = self.session.query(TrafficCount).order_by(desc(TrafficCount.id)).first()
        last_traffic_count = self.session.query(TrafficCount).order_by(asc(TrafficCount.id)).first()
        test_session, error, delete_occurred = backup_db(self.session)
        self.assertIsNone(error)
        self.assertTrue(delete_occurred)
        remaining_count = test_session.query(TrafficCount).count()
        self.assertEqual(remaining_count, 200)
        # check that the entries remaining are the most recent
        second_first_traffic_count = test_session.query(TrafficCount).order_by(desc(TrafficCount.id)).first()
        second_last_traffic_count = test_session.query(TrafficCount).order_by(asc(TrafficCount.id)).first()
        self.assertEqual(second_last_traffic_count, last_traffic_count)
        self.assertNotEqual(second_first_traffic_count, first_traffic_count)

if __name__ == '__main__':
    unittest.main()