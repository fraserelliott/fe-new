from runner import Runner
from cli.prompts import run_prompts, build_actions

def main():
    context = run_prompts()
    runner = build_actions(context)
    runner.execute()

if __name__ == "__main__":
    main()