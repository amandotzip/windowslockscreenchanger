import unittest
from unittest.mock import patch, MagicMock
import os
from main import get_top_x_posts, create_directory, delete_files_at_path, process_default, process_gallery

class TestGetTopXPosts(unittest.TestCase):

    @patch('main.create_directory')
    @patch('main.delete_files_at_path')
    @patch('main.reddit')
    @patch('main.process_default')
    @patch('main.process_gallery')
    def test_get_top_x_posts(self, mock_process_gallery, mock_process_default, mock_reddit, mock_delete_files_at_path, mock_create_directory):
        # Setup
        x = 2
        saved_images_path = "test_path"
        mock_submission1 = MagicMock()
        mock_submission1.url = "http://example.com/image1.jpg"
        mock_submission1.stickied = False
        mock_submission1.link_flair_text = None
        mock_submission1.id = "id1"
        
        mock_submission2 = MagicMock()
        mock_submission2.url = "http://example.com/gallery/image2.jpg"
        mock_submission2.stickied = False
        mock_submission2.link_flair_text = None
        mock_submission2.id = "id2"
        
        mock_reddit.subreddit().hot.return_value = [mock_submission1, mock_submission2]

        # Execute
        get_top_x_posts(x, saved_images_path)

        # Verify
        mock_create_directory.assert_called_once_with(os.path.join(saved_images_path, "images/"))
        mock_delete_files_at_path.assert_called_once_with(os.path.join(saved_images_path, "images/"))
        mock_reddit.subreddit().hot.assert_called_once_with(limit=x)
        mock_process_default.assert_called_once_with(mock_submission1, os.path.join(saved_images_path, "images/"))
        mock_process_gallery.assert_called_once_with(mock_submission2, os.path.join(saved_images_path, "images/"))

if __name__ == '__main__':
    unittest.main()