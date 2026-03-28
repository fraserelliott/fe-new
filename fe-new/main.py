from runner import Runner
from cli.prompts import run_prompts, build_runner
from plugins import *

all_plugins = [FeSlatePlugin(), ReactRouterPlugin(), SequelizePlugin()]

def main():
    context = run_prompts()
    plugin_manager = PluginManager(all_plugins)
    plugin_manager.prompt_for_plugins(context)
    runner = build_runner(context)
    plugin_actions = plugin_manager.build_actions(context)
    runner.add_actions(plugin_actions)
    runner.execute()

if __name__ == "__main__":
    main()