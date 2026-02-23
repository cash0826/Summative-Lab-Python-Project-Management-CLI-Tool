import pytest
from unittest.mock import patch, MagicMock
from lib.controllers.tasks_controller import TasksController
from lib.models.task import Task

class TestTasksController:
    @pytest.fixture
    def sample_tasks_data(self):
        return [
            {
                "title": "Task 1",
                "associated_project": "Project Alpha",
                "assigned_to": "John Doe",
                "status": "Pending"
            },
            {
                "title": "Task 2",
                "associated_project": "Project Alpha",
                "assigned_to": "Jane Smith",
                "status": "Completed"
            }
        ]

    @pytest.fixture
    def sample_projects_data(self):
        return [
            {"title": "Project Alpha", "description": "Test project", "due_date": "12/31/2025", "owner_email": "owner@example.com"},
            {"title": "Project Beta", "description": "Another project", "due_date": "01/15/2026", "owner_email": "owner@example.com"}
        ]

    @pytest.fixture
    def sample_users_data(self):
        return [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"}
        ]

    @pytest.fixture
    def controller(self, tmp_path):
        test_file = tmp_path / "test_tasks.json"
        return TasksController(str(test_file))

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    @patch('builtins.print')
    def test_add_task_success(self, mock_print, mock_save, mock_load, controller, sample_projects_data, sample_users_data):
        """Test successfully adding a new task"""
        # Mock empty tasks data and valid projects/users data
        def load_side_effect(path):
            if "tasks.json" in path:
                return []
            elif "projects.json" in path:
                return sample_projects_data
            else:
                return sample_users_data

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.title = "New Task"
        args.project_title = "Project Alpha"
        args.assigned_to = "John Doe"
        args.status = "In Progress"

        with controller as ctrl:
            result = ctrl.add_task(args)

        assert result is not None
        assert result.title == "New Task"
        assert result.associated_project == "Project Alpha"
        assert result.assigned_to == "John Doe"
        assert result.status == "In Progress"

        mock_print.assert_called_with("Added task: New Task was successfully added to project Project Alpha.")

        mock_save.assert_called_once()

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_add_task_invalid_project(self, mock_print, mock_load, controller, sample_users_data):
        """Test adding task to non-existent project fails"""
        def load_side_effect(path):
            if "tasks.json" in path:
                return []
            elif "projects.json" in path:
                return []  # No projects
            else:
                return sample_users_data

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.title = "New Task"
        args.project_title = "Non-existent Project"
        args.assigned_to = "John Doe"
        args.status = "Pending"

        with controller as ctrl:
            result = ctrl.add_task(args)

        assert result is None
        mock_print.assert_called_with("Error: No project found with title Non-existent Project.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_add_task_invalid_user(self, mock_print, mock_load, controller, sample_projects_data):
        """Test adding task assigned to non-existent user fails"""
        def load_side_effect(path):
            if "tasks.json" in path:
                return []
            elif "projects.json" in path:
                return sample_projects_data
            else:  # users.json
                return []  # No users

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.title = "New Task"
        args.project_title = "Project Alpha"
        args.assigned_to = "Non-existent User"
        args.status = "Pending"

        with controller as ctrl:
            result = ctrl.add_task(args)

        assert result is None
        mock_print.assert_called_with("Error: No user found with email Non-existent User.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_add_task_duplicate_title(self, mock_print, mock_load, controller, sample_tasks_data, sample_projects_data, sample_users_data):
        """Test adding task with duplicate title in same project fails"""
        def load_side_effect(path):
            if "tasks.json" in path:
                return sample_tasks_data
            elif "projects.json" in path:
                return sample_projects_data
            else:
                return sample_users_data

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.title = "Task 1"  # Already exists in Project Alpha
        args.project_title = "Project Alpha"
        args.assigned_to = "John Doe"
        args.status = "Pending"

        with controller as ctrl:
            result = ctrl.add_task(args)

        assert result is None
        mock_print.assert_called_with("Error: A task with title 'Task 1' already exists in project 'Project Alpha'.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_complete_task_success(self, mock_print, mock_load, controller, sample_tasks_data, sample_projects_data):
        """Test successfully completing a task"""
        def load_side_effect(path):
            if "tasks.json" in path:
                return sample_tasks_data
            else:
                return sample_projects_data

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.task = "Task 1"
        args.project_title = "Project Alpha"

        with controller as ctrl:
            result = ctrl.complete_task(args)

        assert result is not None
        assert result["title"] == "Task 1"
        assert result["status"] == "Completed"

        mock_print.assert_called_with("Task 'Task 1' in project 'Project Alpha' marked as completed.✅")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_complete_task_not_found(self, mock_print, mock_load, controller, sample_tasks_data, sample_projects_data):
        """Test completing non-existent task fails"""
        def load_side_effect(path):
            if "tasks.json" in path:
                return sample_tasks_data
            else:
                return sample_projects_data

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.task = "Non-existent Task"
        args.project_title = "Project Alpha"

        with controller as ctrl:
            result = ctrl.complete_task(args)

        assert result is None
        mock_print.assert_called_with("Error: No task found with title 'Non-existent Task' in project 'Project Alpha'.")

    @patch('lib.utils.storage.load_data')
    @patch('builtins.print')
    def test_complete_task_invalid_project(self, mock_print, mock_load, controller, sample_tasks_data):
        """Test completing task in non-existent project fails"""
        def load_side_effect(path):
            if "tasks.json" in path:
                return sample_tasks_data
            else:
                return []  # No projects

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.task = "Task 1"
        args.project_title = "Project Alpha"  # Valid project title from sample data

        with controller as ctrl:
            result = ctrl.complete_task(args)

        assert result is None
        mock_print.assert_called_with("Error: No project found with title Project Alpha.")

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    def test_context_manager_loads_tasks(self, mock_save, mock_load, controller, sample_tasks_data):
        """Test that context manager properly loads task data"""
        mock_load.return_value = sample_tasks_data

        with controller as ctrl:
            # Tasks are stored as raw dicts in the controller
            assert len(ctrl.data) == 2
            assert ctrl.data[0]["title"] == "Task 1"
            assert ctrl.data[0]["status"] == "Pending"

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    def test_context_manager_saves_tasks(self, mock_save, mock_load, controller, sample_tasks_data):
        """Test that context manager properly saves task data on exit"""
        mock_load.return_value = sample_tasks_data

        with controller as ctrl:
            new_task = Task("New Task", "Project Alpha", "John Doe", "Pending")
            ctrl.data.append(new_task.to_dict())

        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][1]
        assert len(saved_data) == 3
        assert saved_data[2]["title"] == "New Task"

    @patch('lib.utils.storage.load_data')
    @patch('lib.utils.storage.save_data')
    @patch('builtins.print')
    def test_add_task_default_status(self, mock_print, mock_save, mock_load, controller, sample_projects_data, sample_users_data):
        """Test that task gets default 'Pending' status when none provided"""
        def load_side_effect(path):
            if "tasks.json" in path:
                return []
            elif "projects.json" in path:
                return sample_projects_data
            else:
                return sample_users_data

        mock_load.side_effect = load_side_effect

        args = MagicMock()
        args.title = "New Task"
        args.project_title = "Project Alpha"
        args.assigned_to = "John Doe"
        args.status = None  # No status provided

        with controller as ctrl:
            result = ctrl.add_task(args)

        assert result is not None
        assert result.status == "Pending"