from backend.database.create_db import Base
from backend.local_processing.auxiliary.aux_program import *
import unittest
from unittest.mock import patch
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

class AuxIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(os.getenv('TEST_SQLITE_DB_LOC'))
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

class TestAuxProgramIntegration(AuxIntegrationTest):
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
        first_traffic_count = self.session.query(TrafficCount).order_by(desc(TrafficCount.id)).first()
        last_traffic_count = self.session.query(TrafficCount).order_by(asc(TrafficCount.id)).first()
        test_session, error, delete_occurred = backup_db(self.session)
        self.assertIsNone(error)
        self.assertTrue(delete_occurred)
        remaining_count = session.query(TrafficCount).count()
        self.assertEqual(remaining_count, 200)
        # check that the entries remaining are the most recent


if __name__ == '__main__':
    unittest.main()