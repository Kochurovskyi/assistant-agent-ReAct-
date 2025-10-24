"""Basic unit tests for the memory agent - 30 essential tests."""
import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage
from datetime import datetime


class TestImports:
    """Test that all modules can be imported."""
    
    def test_import_config(self):
        """Test config module import."""
        from config import Configuration, AppConfig
        assert Configuration is not None
        assert AppConfig is not None
    
    def test_import_utils(self):
        """Test utils modules import."""
        from utils.logging_config import logger
        from utils.metrics import metrics
        from utils.helpers import Sniffer, extract_tool_info
        assert logger is not None
        assert metrics is not None
        assert Sniffer is not None
        assert extract_tool_info is not None
    
    def test_import_schemas(self):
        """Test schema modules import."""
        from schemas.profile import Profile
        from schemas.todo import ToDo
        from schemas.memory import UpdateMemory
        assert Profile is not None
        assert ToDo is not None
        assert UpdateMemory is not None
    
    def test_import_chains(self):
        """Test chains modules import."""
        from chains.prompts import MODEL_SYSTEM_MESSAGE, TRUSTCALL_INSTRUCTION
        from chains.extractors import initialize_model
        assert MODEL_SYSTEM_MESSAGE is not None
        assert TRUSTCALL_INSTRUCTION is not None
        assert initialize_model is not None
    
    def test_import_graph(self):
        """Test graph modules import."""
        from graph.nodes import task_asis, update_profile
        from graph.edges import route_message
        from graph.builder import health_check, get_metrics
        assert task_asis is not None
        assert update_profile is not None
        assert route_message is not None
        assert health_check is not None
        assert get_metrics is not None


class TestConfiguration:
    """Test configuration functionality."""
    
    def test_configuration_defaults(self):
        """Test Configuration default values."""
        from config import Configuration
        config = Configuration()
        assert config.user_id == "default-user"
        assert config.todo_category == "general"
        assert "task management" in config.task_asis_role
    
    def test_configuration_custom(self):
        """Test Configuration with custom values."""
        from config import Configuration
        config = Configuration(
            user_id="test-user",
            todo_category="work",
            task_asis_role="Custom role"
        )
        assert config.user_id == "test-user"
        assert config.todo_category == "work"
        assert config.task_asis_role == "Custom role"
    
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
    def test_app_config(self):
        """Test AppConfig with environment variables."""
        from config import AppConfig
        config = AppConfig()
        assert config.google_api_key == 'test-key'
        assert config.model_name == 'gemini-2.0-flash-lite'


class TestSchemas:
    """Test schema validation."""
    
    def test_profile_schema(self):
        """Test Profile schema."""
        from schemas.profile import Profile
        profile = Profile(name="John", location="SF")
        assert profile.name == "John"
        assert profile.location == "SF"
        assert profile.connections == []
        assert profile.interests == []
    
    def test_todo_schema(self):
        """Test ToDo schema."""
        from schemas.todo import ToDo
        todo = ToDo(
            task="Test task",
            time_to_complete=60,
            solutions=["step1", "step2"]
        )
        assert todo.task == "Test task"
        assert todo.time_to_complete == 60
        assert todo.solutions == ["step1", "step2"]
        assert todo.status == "not started"
    
    def test_todo_status_validation(self):
        """Test ToDo status validation."""
        from schemas.todo import ToDo
        todo = ToDo(
            task="Test task",
            time_to_complete=60,
            solutions=["step1"],
            status="in progress"
        )
        assert todo.status == "in progress"
    
    def test_memory_schema(self):
        """Test UpdateMemory schema."""
        from schemas.memory import UpdateMemory
        memory = UpdateMemory(update_type="user")
        assert memory["update_type"] == "user"


class TestUtils:
    """Test utility functions."""
    
    def test_metrics_initialization(self):
        """Test Metrics initialization."""
        from utils.metrics import Metrics
        metrics = Metrics()
        assert metrics.requests_total == 0
        assert metrics.errors_total == 0
        assert metrics.memory_updates == 0
    
    def test_metrics_recording(self):
        """Test Metrics recording."""
        from utils.metrics import Metrics
        metrics = Metrics()
        metrics.record_request(1.5)
        metrics.record_error()
        metrics.record_memory_update()
        assert metrics.requests_total == 1
        assert metrics.errors_total == 1
        assert metrics.memory_updates == 1
    
    def test_sniffer_initialization(self):
        """Test Sniffer initialization."""
        from utils.helpers import Sniffer
        sniffer = Sniffer()
        assert sniffer.called_tools == []
    
    def test_extract_tool_info(self):
        """Test extract_tool_info function."""
        from utils.helpers import extract_tool_info
        tool_calls = [[{
            'name': 'PatchDoc',
            'args': {
                'json_doc_id': 'doc-123',
                'planned_edits': 'Update document',
                'patches': [{'value': 'New content'}]
            }
        }]]
        result = extract_tool_info(tool_calls)
        assert 'Document doc-123 updated:' in result
        assert 'New content' in result


class TestChains:
    """Test chain components."""
    
    def test_prompts_formatting(self):
        """Test prompt template formatting."""
        from chains.prompts import MODEL_SYSTEM_MESSAGE, TRUSTCALL_INSTRUCTION
        formatted = MODEL_SYSTEM_MESSAGE.format(
            task_asis_role="Test role",
            user_profile="Test profile",
            todo="Test todo",
            instructions="Test instructions"
        )
        assert "Test role" in formatted
        assert "Test profile" in formatted
    
    def test_trustcall_instruction(self):
        """Test TRUSTCALL_INSTRUCTION formatting."""
        from chains.prompts import TRUSTCALL_INSTRUCTION
        formatted = TRUSTCALL_INSTRUCTION.format(time="2024-01-01T00:00:00")
        assert "2024-01-01T00:00:00" in formatted
        assert "Reflect on following interaction" in formatted


class TestGraph:
    """Test graph components."""
    
    def test_route_message_no_tool_calls(self):
        """Test route_message with no tool calls."""
        from graph.edges import route_message
        from langgraph.graph import END
        state = {"messages": [MagicMock(tool_calls=[])]}
        result = route_message(state, {}, MagicMock())
        assert result == END
    
    def test_route_message_user_update(self):
        """Test route_message with user update."""
        from graph.edges import route_message
        mock_tool_call = MagicMock()
        mock_tool_call.__getitem__.return_value = {"update_type": "user"}
        state = {"messages": [MagicMock(tool_calls=[mock_tool_call])]}
        result = route_message(state, {}, MagicMock())
        assert result == "update_profile"
    
    def test_route_message_todo_update(self):
        """Test route_message with todo update."""
        from graph.edges import route_message
        mock_tool_call = MagicMock()
        mock_tool_call.__getitem__.return_value = {"update_type": "todo"}
        state = {"messages": [MagicMock(tool_calls=[mock_tool_call])]}
        result = route_message(state, {}, MagicMock())
        assert result == "update_todos"
    
    def test_health_check(self):
        """Test health check function."""
        from graph.builder import health_check
        with patch('graph.builder.InMemoryStore') as mock_store_class:
            mock_store = MagicMock()
            mock_store_class.return_value = mock_store
            mock_store.put.return_value = None
            mock_store.get.return_value = MagicMock()
            
            result = health_check()
            assert result["status"] == "healthy"
            assert "timestamp" in result
            assert "store_connectivity" in result
    
    def test_get_metrics(self):
        """Test get_metrics function."""
        from graph.builder import get_metrics
        with patch('graph.builder.metrics') as mock_metrics:
            mock_stats = {"requests_total": 5, "errors_total": 0}
            mock_metrics.get_stats.return_value = mock_stats
            result = get_metrics()
            assert result == mock_stats


class TestIntegration:
    """Test integration functionality."""
    
    def test_main_imports(self):
        """Test main module imports."""
        from graph.builder import graph, health_check, get_metrics
        from tests.test_agent import test_production_agent
        assert graph is not None
        assert health_check is not None
        assert get_metrics is not None
        assert test_production_agent is not None
    
    def test_graph_has_required_attributes(self):
        """Test graph has required attributes."""
        from graph.builder import graph
        assert hasattr(graph, 'stream')
        assert hasattr(graph, 'store')
        assert hasattr(graph, 'checkpointer')
    
    def test_environment_configuration(self):
        """Test environment-based configuration."""
        with patch.dict('os.environ', {
            'GOOGLE_API_KEY': 'test-key',
            'MODEL_NAME': 'test-model',
            'LOG_LEVEL': 'DEBUG'
        }):
            from config import AppConfig
            config = AppConfig()
            assert config.google_api_key == 'test-key'
            assert config.model_name == 'test-model'
            assert config.log_level == 'DEBUG'
    
    def test_logging_configuration(self):
        """Test logging is configured."""
        from utils.logging_config import logger
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
    
    def test_metrics_tracking(self):
        """Test metrics tracking works."""
        from utils.metrics import metrics
        # Reset metrics for clean test
        metrics.requests_total = 0
        metrics.errors_total = 0
        metrics.memory_updates = 0
        
        metrics.record_request(1.0)
        metrics.record_error()
        metrics.record_memory_update()
        
        assert metrics.requests_total == 1
        assert metrics.errors_total == 1
        assert metrics.memory_updates == 1
        
        stats = metrics.get_stats()
        assert "requests_total" in stats
        assert "errors_total" in stats
        assert "memory_updates" in stats
    
    def test_retry_decorator(self):
        """Test retry decorator functionality."""
        from utils.helpers import retry_on_failure
        call_count = 0
        
        @retry_on_failure(max_retries=2, delay=0.01)
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Temporary failure")
            return "success"
        
        result = flaky_function()
        assert result == "success"
        assert call_count == 2
    
    def test_prompts_content(self):
        """Test that prompts contain expected content."""
        from chains.prompts import MODEL_SYSTEM_MESSAGE, TRUSTCALL_INSTRUCTION, CREATE_INSTRUCTIONS
        assert "long term memory" in MODEL_SYSTEM_MESSAGE
        assert "user's profile" in MODEL_SYSTEM_MESSAGE
        assert "ToDo list" in MODEL_SYSTEM_MESSAGE
        assert "Reflect on following interaction" in TRUSTCALL_INSTRUCTION
        assert "update your instructions" in CREATE_INSTRUCTIONS
