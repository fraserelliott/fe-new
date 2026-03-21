from runner import Runner
from cli.prompts import run_prompts

def main():
    context = run_prompts()
    runner = build_actions(context)
    runner.execute()

def build_actions(context):
    runner = Runner(context)

    return runner

if __name__ == "__main__":
    main()