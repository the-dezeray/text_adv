# test if all are decorated

import pytest
from unittest.mock import Mock, patch
from core.core import Core
from core.events import *

@pytest.fixture
def mock_core():
    core = Mock(spec=Core)
    core.console = Mock()
    core.player = Mock()
    core.entity = Mock()
    core.goto_next = Mock()
    return core

def test_navigate(mock_core):
    rest(mock_core)
    mock_core.console.clear_display.assert_called_once()
    mock_core.console.print.assert_called()

