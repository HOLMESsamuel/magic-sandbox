class WebSocketManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebSocketManager, cls).__new__(cls)
            cls._instance.connected_groups = {}
        return cls._instance

    async def broadcast(self, group_id: str, state):
        for client in self.connected_groups.get(group_id, []):
            try:
                await client.send_json(state)
            except Exception:
                # Handle failed send (e.g., client disconnected)
                pass


    def add_connection(self, group_id: str, websocket):
        if group_id not in self.connected_groups:
            self.connected_groups[group_id] = []
        self.connected_groups[group_id].append(websocket)

    def remove_connection(self, group_id: str, websocket):
        if group_id in self.connected_groups:
            self.connected_groups[group_id].remove(websocket)
            if not self.connected_groups[group_id]:
                del self.connected_groups[group_id]
