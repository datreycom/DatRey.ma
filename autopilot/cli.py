import argparse
import sys
from autopilot.orchestrator import run_autopilot_cycle

def main():
    parser = argparse.ArgumentParser(description="DatRey Autopilot Content Engine")
    parser.add_argument("--auto", action="store_true", help="Run daily quota based on active week schedule")
    parser.add_argument("--count", type=int, default=None, help="Force specific number of articles to generate")
    parser.add_argument("--topic", type=str, default=None, help="Optional topic hint for article generation")

    args = parser.parse_args()

    if not args.auto and args.count is None:
        # Default to auto mode if no flags passed
        print("No flags provided. Defaulting to --auto mode.")
        args.auto = True

    run_autopilot_cycle(force_count=args.count, topic_hint=args.topic)

if __name__ == "__main__":
    main()
