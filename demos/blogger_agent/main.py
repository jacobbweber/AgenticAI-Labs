"""
Main CLI Entrypoint for Headless Blogger Agent
"""

import json

from core.orchestrator import BloggerOrchestrator


def main():
    print("=" * 60)
    print("Starting Headless Autonomous Blogger Agent Run...")
    print("=" * 60)

    orchestrator = BloggerOrchestrator()
    results = orchestrator.run_pipeline()

    print("\nRun Summary:")
    print(json.dumps(results, indent=2))
    print("=" * 60)


if __name__ == "__main__":
    main()
