

import pytest
import json
import os
from unittest.mock import patch, mock_open, MagicMock, call
from lib.controllers.users_controllers import UsersControllers
from lib.models.user import User


class TestUsersControllers:
    @pytest.fixture
    def sample_users_data(self):
        return [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"}
        ]

    @pytest.fixture
    def controller(self, tmp_path):
        # Create a temporary file for testing
        test_file = tmp_path / "test_users.json"
        return UsersControllers(str(test_file))

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    @patch('builtins.print')
    def test_add_user_success(self, mock_print, mock_save, mock_load, controller, sample_users_data):
        """Test successfully adding a new user"""
        # Mock empty data (no existing users)
        mock_load.return_value = []

        # Create mock args
        args = MagicMock()
        args.name = "Alice Johnson"
        args.email = "alice@example.com"

        with controller as ctrl:
            result = ctrl.add_user(args)

        # Verify the user was created
        assert result is not None
        assert result.name == "Alice Johnson"
        assert result.email == "alice@example.com"

        # Verify success message was printed
        mock_print.assert_called_with("Added user: Alice Johnson was successfully added: {'name': 'Alice Johnson', 'email': 'alice@example.com'}")

        # Verify data was saved
        mock_save.assert_called_once()

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_add_user_duplicate_email(self, mock_print, mock_load, controller, sample_users_data):
        """Test adding a user with duplicate email fails gracefully"""
        # Mock existing users data
        mock_load.return_value = sample_users_data

        # Create mock args with existing email
        args = MagicMock()
        args.name = "New User"
        args.email = "john@example.com"  # Already exists

        with controller as ctrl:
            result = ctrl.add_user(args)

        # Verify None was returned (failure)
        assert result is None

        # Verify error message was printed
        mock_print.assert_called_with("Error: User with email john@example.com already exists.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_list_users_with_data(self, mock_print, mock_load, controller, sample_users_data):
        """Test listing users when data exists"""
        mock_load.return_value = sample_users_data

        with controller as ctrl:
            result = ctrl.list_users()

        # Verify users were returned
        assert len(result) == 2
        assert all(isinstance(user, User) for user in result)

        # Verify output was printed
        expected_calls = [
            call("Users:\nJohn Doe, <john@example.com>"),
            call("Users:\nJane Smith, <jane@example.com>")
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_list_users_empty(self, mock_print, mock_load, controller):
        """Test listing users when no users exist"""
        mock_load.return_value = []

        with controller as ctrl:
            result = ctrl.list_users()

        # Verify empty list was returned
        assert result == []

        # Verify no users message was printed
        mock_print.assert_called_with("No users found.")

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    def test_context_manager_loads_data(self, mock_print, mock_load, controller, sample_users_data):
        """Test that context manager properly loads and converts data"""
        mock_load.return_value = sample_users_data

        with controller as ctrl:
            # Data should be loaded and converted to User objects
            assert len(ctrl.data) == 2
            assert all(isinstance(user, User) for user in ctrl.data)
            assert ctrl.data[0].name == "John Doe"
            assert ctrl.data[0].email == "john@example.com"

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    def test_context_manager_saves_data(self, mock_save, mock_load, controller, sample_users_data):
        """Test that context manager properly saves data on exit"""
        mock_load.return_value = sample_users_data

        with controller as ctrl:
            # Modify data
            ctrl.data.append(User("New User", "new@example.com"))

        # Verify save was called with converted data
        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][1]  # Second argument is the data
        assert len(saved_data) == 3
        assert saved_data[2] == {"name": "New User", "email": "new@example.com"}