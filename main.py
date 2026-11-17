"""
Compass - AI Campus Assistant
Course : AIP203 - Artificial Intelligence Lab (Mini Project)

Run   : python main.py                  -> web interface (opens in your browser)
        python main.py --cli            -> terminal chat
        python main.py --port 9000      -> choose the web port
        python main.py --no-browser     -> do not open the browser automatically
"""
import argparse

from assistant import ui

BANNER = r"""
  ____
 / ___|  ___   _ __ ___    _ __     __ _  ___   ___
| |     / _ \ | '_ ` _ \  | '_ \   / _` |/ __| / __|
| |___ | (_) || | | | | | | |_) | | (_| |\__ \ \__ \
 \____| \___/ |_| |_| |_| | .__/   \__,_||___/ |___/
                          |_|

   AI Campus Assistant   |   AIP203 AI Lab
"""


def run_cli():
    from assistant.core import run
    print(ui.color("header", BANNER))
    print(ui.color("warn", "  Hello! I'm Compass. Ask me about routes, tasks, maths, weather..."))
    print(ui.color("ok", "  Type 'help' for commands, 'demo' for AI algorithm demos, 'exit' to quit.\n"))
    try:
        run()
    except KeyboardInterrupt:
        print("\n  [Compass] Goodbye!\n")


def main():
    parser = argparse.ArgumentParser(description="Compass - AI Campus Assistant")
    parser.add_argument("--cli", action="store_true", help="use the terminal instead of the web interface")
    parser.add_argument("--port", type=int, default=8000, help="web interface port (default 8000)")
    parser.add_argument("--no-browser", action="store_true", help="do not open the browser automatically")
    args = parser.parse_args()
    if args.cli:
        run_cli()
    else:
        from assistant.webui import launch
        launch(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
