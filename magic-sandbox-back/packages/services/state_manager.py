class StateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance.group_states = {}
        return cls._instance

    def update_group_state(self, group_id, state):
        self.group_states[group_id] = state

    def get_group_state(self, group_id):
        return self.group_states.get(group_id)

    def delete_group_state(self, group_id):
        if group_id in self.group_states:
            del self.group_states[group_id]


