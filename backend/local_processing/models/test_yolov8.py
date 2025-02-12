import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import torch
from YOLOv8 import preprocess_image, infer, extract_vehicle_count, process_image


class TestImageProcessing(unittest.TestCase):

    @patch("cv2.imread", return_value=np.ones((800, 800, 3), dtype=np.uint8))
    @patch("cv2.resize")
    @patch("cv2.cvtColor")
    @patch("YOLOv8.enable_grayscale", True)
    def test_preprocess_image_grayscale_enabled(self, mock_cvtColor, mock_resize, mock_imread):
        """Test image preprocessing including resizing and grayscale conversion."""
        mock_resize.side_effect = lambda img, size: np.ones((640, 640, 3), dtype=np.uint8)
        mock_cvtColor.side_effect = lambda img, code: img  # Mock grayscale conversion

        image = preprocess_image("dummy_path.jpg")

        self.assertEqual(image.shape, (640, 640, 3))
        mock_imread.assert_called_once_with("dummy_path.jpg")
        mock_resize.assert_called_once()
        mock_cvtColor.assert_called()

    @patch("cv2.imread", return_value=np.ones((800, 800, 3), dtype=np.uint8))
    @patch("cv2.resize")
    @patch("cv2.cvtColor")
    @patch("YOLOv8.enable_grayscale", False)
    def test_preprocess_image_grayscale_disabled(self, mock_cvtColor, mock_resize, mock_imread):
        """Test image preprocessing including resizing and grayscale conversion."""
        mock_resize.side_effect = lambda img, size: np.ones((640, 640, 3), dtype=np.uint8)
        mock_cvtColor.side_effect = lambda img, code: img  # Mock grayscale conversion

        image = preprocess_image("dummy_path.jpg")

        self.assertEqual(image.shape, (640, 640, 3))
        mock_imread.assert_called_once_with("dummy_path.jpg")
        mock_resize.assert_called_once()
        mock_cvtColor.assert_not_called()

    @patch("torch.cuda.is_available", return_value=False)
    @patch("YOLOv8.YOLO")
    def test_infer_cuda_unavailable(self, mock_YOLO, mock_cuda_available):
        """Test inference with YOLO model."""
        mock_model = MagicMock()
        mock_model.to.return_value = mock_model
        mock_model.return_value = [MagicMock(boxes=MagicMock(data=torch.tensor([[10, 10, 50, 50, 0.8, 1]])))]
        mock_YOLO.return_value = mock_model

        results = infer("dummy_image", "dummy_weights.pt")

        self.assertTrue(torch.equal(results, torch.tensor([[10, 10, 50, 50, 0.8, 1]])))
        mock_YOLO.assert_called_once_with("dummy_weights.pt")
        mock_model.to.assert_called_once_with("cpu")

    @patch("torch.cuda.is_available", return_value=True)
    @patch("YOLOv8.YOLO")
    def test_infer_cuda_available(self, mock_YOLO, mock_cuda_available):
        """Test inference with YOLO model."""
        mock_model = MagicMock()
        mock_model.to.return_value = mock_model
        mock_model.return_value = [MagicMock(boxes=MagicMock(data=torch.tensor([[10, 10, 50, 50, 0.8, 1]])))]
        mock_YOLO.return_value = mock_model

        results = infer("dummy_image", "dummy_weights.pt")

        self.assertTrue(torch.equal(results, torch.tensor([[10, 10, 50, 50, 0.8, 1]])))
        mock_YOLO.assert_called_once_with("dummy_weights.pt")
        mock_model.to.assert_called_once_with("cuda")

    def test_extract_vehicle_count_detections(self):
        """Test vehicle counting with confidence filtering."""
        detections = torch.tensor([
            [10, 10, 50, 50, 0.9, 1],  # High confidence
            [20, 20, 60, 60, 0.5, 2],  # medium confidence
            [30, 30, 70, 70, 0.2, 3]  # Below confidence threshold
        ])
        count = extract_vehicle_count(detections, confidence=0.3)
        self.assertEqual(count, 2)

    def test_extract_vehicle_count_empty(self):
        """Test vehicle counting with confidence filtering."""
        detections = torch.tensor([])
        count = extract_vehicle_count(detections, confidence=0.3)
        self.assertEqual(count, 0)

    @patch("YOLOv8.preprocess_image")
    @patch("YOLOv8.infer")
    @patch("YOLOv8.save_detections_to_disk")
    @patch("YOLOv8.extract_vehicle_count")
    def test_process_image_save_to_disk_enabled(self, mock_extract, mock_save, mock_infer, mock_preprocess):
        """Test full process workflow, including saving and counting."""
        mock_preprocess.return_value = np.ones((640, 640, 3), dtype=np.uint8)
        mock_infer.return_value = torch.tensor([[10, 10, 50, 50, 0.9, 1]])
        mock_extract.return_value = 1

        count = process_image("dummy.jpg", "dummy_weights.pt", confidence=0.8, save_to_disk=True,
                              model_name="yolo", conditions="daylight", image_name="test.jpg")

        self.assertEqual(count, 1)
        mock_preprocess.assert_called_once_with("dummy.jpg")
        mock_infer.assert_called_once()
        mock_extract.assert_called_once()
        mock_save.assert_called_once()  # Ensuring the detection is saved

    @patch("YOLOv8.preprocess_image")
    @patch("YOLOv8.infer")
    @patch("YOLOv8.save_detections_to_disk")
    @patch("YOLOv8.extract_vehicle_count")
    def test_process_image_save_to_disk_disabled(self, mock_extract, mock_save, mock_infer, mock_preprocess):
        """Test full process workflow, including saving and counting."""
        mock_preprocess.return_value = np.ones((640, 640, 3), dtype=np.uint8)
        mock_infer.return_value = torch.tensor([[10, 10, 50, 50, 0.9, 1]])
        mock_extract.return_value = 1

        count = process_image("dummy.jpg", "dummy_weights.pt", confidence=0.8, save_to_disk=False,
                              model_name="yolo", conditions="daylight", image_name="test.jpg")

        self.assertEqual(count, 1)
        mock_preprocess.assert_called_once_with("dummy.jpg")
        mock_infer.assert_called_once()
        mock_extract.assert_called_once()
        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
