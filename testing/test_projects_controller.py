import pytest
from datetime import date
from unittest.mock import patch, MagicMock, call
from lib.controllers.projects_controller import ProjectsControllers
from lib.models.project import Project

class TestProjectsControllers:
    @pytest.fixture
    def sample_projects_data(self):
        return [
            {
                "title": "Project Alpha",
                "description": "First project",
                "due_date": "12/31/2025",
                "owner_email": "owner@example.com"
            },
            {
                "title": "Project Beta",
                "description": "Second project",
                "due_date": "01/15/2026",
                "owner_email": "owner@example.com"
            }
        ]

    @pytest.fixture
    def sample_users_data(self):
        return [
            {"name": "Owner", "email": "owner@example.com"},
            {"name": "User", "email": "user@example.com"}
        ]

    @pytest.fixture
    def controller(self, tmp_path):
        test_file = tmp_path / "test_projects.json"
        return ProjectsControllers(str(test_file))

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    @patch('builtins.print')
    def test_add_project_success(self, mock_print, mock_save, mock_load, controller, sample_users_data):
        """Test successfully adding a new project"""
        # Mock empty projects data and valid users data
        mock_load.side_effect = lambda path: [] if "projects.json" in path else sample_users_data

        # Create mock args
        args = MagicMock()
        args.title = "New Project"
        args.description = "A new test project"
        args.due_date = "03/15/2026"
        args.owner_email = "owner@example.com"

        with controller as ctrl:
            result = ctrl.add_project(args)

        # Verify the project was created
        assert result is not None
        assert result.title == "New Project"
        assert result.description == "A new test project"
        assert result.due_date == date(2026, 3, 15)
        assert result.owner_email == "owner@example.com"

        # Verify success message was printed
        mock_print.assert_called_with("Added project: New Project was successfully added: {'title': 'New Project', 'description': 'A new test project', 'due_date': '03/15/2026', 'owner_email': 'owner@example.com'}")

        # Verify data was saved
        mock_save.assert_called_once()

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_add_project_invalid_owner_email(self, mock_print, mock_load, controller):
        """Test adding project with non-existent owner email fails"""
        # Mock empty projects and users data (no matching email)
        mock_load.side_effect = lambda path: [] if "projects.json" in path else []

        args = MagicMock()
        args.title = "New Project"
        args.description = "Test project"
        args.due_date = "03/15/2026"
        args.owner_email = "nonexistent@example.com"

        with controller as ctrl:
            result = ctrl.add_project(args)

        assert result is None
        mock_print.assert_called_with("Error: No user found with email nonexistent@example.com.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_add_project_duplicate_title(self, mock_print, mock_load, controller, sample_projects_data, sample_users_data):
        """Test adding project with duplicate title fails"""
        mock_load.side_effect = lambda path: sample_projects_data if "projects.json" in path else sample_users_data

        args = MagicMock()
        args.title = "Project Alpha"  # Already exists
        args.description = "Duplicate project"
        args.due_date = "03/15/2026"
        args.owner_email = "owner@example.com"

        with controller as ctrl:
            result = ctrl.add_project(args)

        assert result is None
        mock_print.assert_called_with("Error: A project with the title 'Project Alpha' already exists.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_add_project_invalid_date_format(self, mock_print, mock_load, controller, sample_users_data):
        """Test adding project with invalid date format fails"""
        mock_load.side_effect = lambda path: [] if "projects.json" in path else sample_users_data

        args = MagicMock()
        args.title = "New Project"
        args.description = "Test project"
        args.due_date = "invalid-date"
        args.owner_email = "owner@example.com"

        with controller as ctrl:
            result = ctrl.add_project(args)

        assert result is None
        mock_print.assert_called_with("Due Date needs to be in this date format: MM/DD/YYYY")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_list_projects_by_owner_success(self, mock_print, mock_load, controller, sample_projects_data, sample_users_data):
        """Test listing projects for existing user with projects"""
        mock_load.side_effect = lambda path: sample_projects_data if "projects.json" in path else sample_users_data

        args = MagicMock()
        args.owner_email = "owner@example.com"

        with controller as ctrl:
            result = ctrl.list_projects_by_owner(args)

        assert len(result) == 2
        assert all(isinstance(project, Project) for project in result)

        # Verify projects were printed
        expected_calls = [
            call("[Project] Title: Project Alpha, Description: First project, Due Date: 2025-12-31"),
            call("[Project] Title: Project Beta, Description: Second project, Due Date: 2026-01-15")
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_list_projects_by_owner_no_user(self, mock_print, mock_load, controller, sample_projects_data):
        """Test listing projects for non-existent user fails"""
        mock_load.side_effect = lambda path: sample_projects_data if "projects.json" in path else []

        args = MagicMock()
        args.owner_email = "nonexistent@example.com"

        with controller as ctrl:
            result = ctrl.list_projects_by_owner(args)

        assert result == []
        mock_print.assert_called_with("Error: No user found with email nonexistent@example.com.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_list_projects_by_owner_no_projects(self, mock_print, mock_load, controller, sample_users_data):
        """Test listing projects for user with no projects"""
        mock_load.side_effect = lambda path: [] if "projects.json" in path else sample_users_data

        args = MagicMock()
        args.owner_email = "owner@example.com"

        with controller as ctrl:
            result = ctrl.list_projects_by_owner(args)

        assert result == []
        mock_print.assert_called_with("No projects found for user with email owner@example.com.")

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    def test_context_manager_loads_projects(self, mock_save, mock_load, controller, sample_projects_data):
        """Test that context manager properly loads and converts project data"""
        mock_load.return_value = sample_projects_data

        with controller as ctrl:
            assert len(ctrl.data) == 2
            assert all(isinstance(project, Project) for project in ctrl.data)
            assert ctrl.data[0].title == "Project Alpha"
            assert ctrl.data[0].due_date == date(2025, 12, 31)

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    def test_context_manager_saves_projects(self, mock_save, mock_load, controller, sample_projects_data):
        """Test that context manager properly saves project data on exit"""
        mock_load.return_value = sample_projects_data

        with controller as ctrl:
            ctrl.data.append(Project("New Project", "Description", date(2026, 6, 1), "owner@example.com"))

        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][1]
        assert len(saved_data) == 3
        assert saved_data[2]["title"] == "New Project"