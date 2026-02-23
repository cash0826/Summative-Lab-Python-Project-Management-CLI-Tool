import pytest
from unittest.mock import patch, MagicMock
from lib.utils.args import parse_args

class TestArgsParsing:
    """Test the argument parsing functionality"""

    @patch('sys.argv', ['main.py', 'user', 'add-user', '-n', 'Test User', '-e', 'test@example.com'])
    def test_parse_add_user_args(self):
        """Test parsing add user command arguments"""
        args = parse_args()

        assert args.command == 'user'
        assert args.user_command == 'add-user'
        assert args.name == 'Test User'
        assert args.email == 'test@example.com'

    @patch('sys.argv', ['main.py', 'user', 'list-users'])
    def test_parse_list_users_args(self):
        """Test parsing list users command arguments"""
        args = parse_args()

        assert args.command == 'user'
        assert args.user_command == 'list-users'

    @patch('sys.argv', ['main.py', 'project', 'add-project', '-t', 'Test Project', '-d', 'Description', '-due', '12/31/2025', '-owner', 'owner@example.com'])
    def test_parse_add_project_args(self):
        """Test parsing add project command arguments"""
        args = parse_args()

        assert args.command == 'project'
        assert args.project_command == 'add-project'
        assert args.title == 'Test Project'
        assert args.description == 'Description'
        assert args.due_date == '12/31/2025'
        assert args.owner_email == 'owner@example.com'

    @patch('sys.argv', ['main.py', 'project', 'list-projects', '-owner', 'owner@example.com'])
    def test_parse_list_projects_args(self):
        """Test parsing list projects command arguments"""
        args = parse_args()

        assert args.command == 'project'
        assert args.project_command == 'list-projects'
        assert args.owner_email == 'owner@example.com'

    @patch('sys.argv', ['main.py', 'task', 'add-task', '-t', 'Test Task', '-p', 'Test Project', '-a', 'user@example.com', '-s', 'Pending'])
    def test_parse_add_task_args(self):
        """Test parsing add task command arguments"""
        args = parse_args()

        assert args.command == 'task'
        assert args.task_command == 'add-task'
        assert args.title == 'Test Task'
        assert args.project_title == 'Test Project'
        assert args.assigned_to == 'user@example.com'
        assert args.status == 'Pending'

    @patch('sys.argv', ['main.py', 'task', 'complete-task', '-t', 'Test Task', '-p', 'Test Project'])
    def test_parse_complete_task_args(self):
        """Test parsing complete task command arguments"""
        args = parse_args()

        assert args.command == 'task'
        assert args.task_command == 'complete-task'
        assert args.task == 'Test Task'
        assert args.project_title == 'Test Project'

    @patch('sys.argv', ['main.py'])
    def test_parse_no_args(self):
        """Test parsing with no arguments"""
        args = parse_args()

        assert args.command is None