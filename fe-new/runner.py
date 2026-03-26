class Runner:
    def __init__(self, context):
        self.context = context
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def add_actions(self, actions):
        self.actions.extend(actions)

    def execute(self):
        self.actions.sort(key=lambda action: action.phase)
        for action in self.actions:
            result = action.execute(self.context)
            if not result.success:
                print(result.message)
                break