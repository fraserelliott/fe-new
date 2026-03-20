class Runner:
    def __init__(self, context):
        self.context = context
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def add_actions(self, actions):
        self.actions.extend(actions)

    def execute(self):
        for action in self.actions:
            action.execute(self.context)