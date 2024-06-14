import unittest
from unittest.mock import patch
from setup_project import main

class TestSetupProject(unittest.TestCase):

    @patch('builtins.input', return_value='valid_project')
    @patch('setup_project.check_python3_installed')
    @patch('setup_project.verify_folder_name')
    @patch('setup_project.manage_folder', return_value=True)
    @patch('setup_project.create_pipfile')
    @patch('setup_project.create_gitignore')
    @patch('logging.info')
    def test_main_success(self, mock_log, mock_gitignore, mock_pipfile, mock_manage_folder, mock_verify, mock_check, mock_input):
        main()
        mock_check.assert_called_once()
        mock_input.assert_called_once()
        mock_verify.assert_called_once_with('valid_project')
        mock_manage_folder.assert_called_once_with('valid_project')
        mock_pipfile.assert_called_once_with('valid_project')
        mock_gitignore.assert_called_once_with('valid_project')
        mock_log.assert_called_with("Setup will proceed using the folder: valid_project")

    @patch('builtins.input', return_value='valid_project')
    @patch('setup_project.check_python3_installed')
    @patch('setup_project.verify_folder_name')
    @patch('setup_project.manage_folder', return_value=False)
    @patch('logging.info')
    def test_main_cancelled_by_user(self, mock_log, mock_manage_folder, mock_verify, mock_check, mock_input):
        main()
        mock_check.assert_called_once()
        mock_input.assert_called_once()
        mock_verify.assert_called_once_with('valid_project')
        mock_manage_folder.assert_called_once_with('valid_project')
        mock_log.assert_called_with("Setup was cancelled by the user.")

if __name__ == '__main__':
    unittest.main()