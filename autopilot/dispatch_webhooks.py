"""
DatRey Autopilot — Post-Deploy Webhook Dispatcher

This module is executed as a separate GitHub Actions step AFTER git push.
It waits for GitHub Pages to deploy, verifies image URLs are live,
then dispatches pending webhooks to Make.com one by one with delays.

Usage:
    python -m autopilot.dispatch_webhooks
"""

from autopilot.social_publisher_service import dispatch_pending_webhooks

if __name__ == "__main__":
    print("=" * 60)
    print("[DatRey Post-Deploy Dispatcher] Starting...")
    print("=" * 60)
    dispatch_pending_webhooks()
    print("[DatRey Post-Deploy Dispatcher] Done.")
