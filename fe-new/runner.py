from actions import Action
from setup_context import SetupContext

class Runner:
    def __init__(self, context: SetupContext):
        self.context = context
        self.actions = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def add_actions(self, actions: list[Action]):
        self.actions.extend(actions)

    def execute(self):
        self.actions.sort(key=lambda action: action.phase)
        for action in self.actions:
            result = action.execute(self.context)
            if not result.success:
                print(result.message)
                break