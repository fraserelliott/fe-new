from .base import Plugin
from setup_context import SetupContext
from actions import Action
from utils.prompting import ask_multi_select

class PluginManager:
    def __init__(self, plugins: list[Plugin]):
        self.all_plugins = plugins
        self.selected_plugins: list[Plugin] = []

    def prompt_for_plugins(self, context: SetupContext) -> None:
        available_plugins = [p for p in self.all_plugins if p.is_available(context)]
        print(f"{len(available_plugins)} available plugins")
        if len(available_plugins) == 0:
            print("No available plugins for the selected project setup. Skipping plugin configuration.")
            return
        choices = [
            {
                "name": f"{plugin.display_name} - {plugin.description}",
                "value": plugin.key
            }
            for plugin in available_plugins
        ]
        selected_keys = ask_multi_select("Select plugins:", choices)
        plugin_map = {p.key: p for p in available_plugins}
        self.selected_plugins = [plugin_map[k] for k in selected_keys]

    def build_actions(self, context: SetupContext) -> list[Action]:
        actions = []
        for plugin in self.selected_plugins:
            actions.extend(plugin.build_actions(context))
        return actions