import unittest
from unittest.mock import patch
import numpy as np
from BoundingBoxes import box_label, plot_bboxes, save_detections_to_disk


class TestBoundingBoxes(unittest.TestCase):

    def setUp(self):
        self.test_image = np.ones((640, 640, 3), dtype=np.uint8) * 255  # White image
        self.test_box = [100, 100, 200, 200, 0.9]  # Sample bounding box

    @patch("cv2.rectangle")
    @patch("cv2.putText")
    def test_box_label(self, mock_putText, mock_rectangle):
        box_label(self.test_image, self.test_box, label='Test Label')
        mock_rectangle.assert_called()  # Ensures a rectangle was drawn
        mock_putText.assert_called()  # Ensures text was placed on image

    def test_plot_bboxes(self):
        boxes = [self.test_box]
        modified_image = plot_bboxes(self.test_image, boxes, conf=0.5)
        self.assertEqual(modified_image.shape, (640, 640, 3))  # Ensure image shape remains same

    @patch("cv2.imwrite")
    @patch("BoundingBoxes.plot_bboxes", return_value=np.ones((640, 640, 3), dtype=np.uint8) * 255)
    @patch("os.mkdir")
    @patch("os.path.exists", return_value=False)
    def test_save_detections_to_disk_path_does_not_exist(self, mock_exists, mock_mkdir, mock_plot_bboxes, mock_imwrite):
        save_detections_to_disk(self.test_image, "test", [self.test_box], 0.5, "model", "daylight")
        mock_exists.assert_called_once_with("Detections\\")  # Check directory existence
        mock_mkdir.assert_called_once_with("Detections\\")  # Ensure mkdir was called
        mock_imwrite.assert_called()  # Ensure image was written to disk

    @patch("cv2.imwrite")
    @patch("BoundingBoxes.plot_bboxes", return_value=np.ones((640, 640, 3), dtype=np.uint8) * 255)
    @patch("os.mkdir")
    @patch("os.path.exists", return_value=True)
    def test_save_detections_to_disk_path_exists(self, mock_exists, mock_mkdir, mock_plot_bboxes, mock_imwrite):
        save_detections_to_disk(self.test_image, "test", [self.test_box], 0.5, "model", "daylight")
        mock_exists.assert_called_once_with("Detections\\")  # Check directory existence
        mock_mkdir.assert_not_called()  # Ensure mkdir was not called
        mock_imwrite.assert_called()  # Ensure image was written to disk


if __name__ == "__main__":
    unittest.main()
