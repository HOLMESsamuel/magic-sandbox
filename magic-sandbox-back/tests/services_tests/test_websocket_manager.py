from unittest.mock import MagicMock
from packages.services.websocket_manager import WebSocketManager

def test_remove_connection():
    manager = WebSocketManager()
    ws1 = MagicMock()  # Mock WebSocket connection
    ws2 = MagicMock()  # Another mock WebSocket connection
    group_id = "test_group"
    manager.connected_groups[group_id] = [ws1, ws2]

    # Execution: Remove one WebSocket connection
    manager.remove_connection(group_id, ws1)

    # Assertion: Verify ws1 is removed but group still exists
    assert ws1 not in manager.connected_groups[group_id]
    assert group_id in manager.connected_groups

    # Execution: Remove the last WebSocket connection
    manager.remove_connection(group_id, ws2)

    # Assertion: Verify the group is deleted after the last connection is removed
    assert group_id not in manager.connected_groups