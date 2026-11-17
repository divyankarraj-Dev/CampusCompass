"""Tiny terminal-colour helper (works without colorama)."""
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    _STYLES = {
        "header": Fore.CYAN + Style.BRIGHT, "prompt": Fore.CYAN + Style.BRIGHT,
        "bot": Fore.GREEN + Style.BRIGHT, "warn": Fore.YELLOW, "ok": Fore.GREEN,
        "err": Fore.RED, "dim": Style.DIM,
    }
    _RESET = Style.RESET_ALL
except ImportError:
    _STYLES, _RESET = {}, ""


def color(kind, text):
    return f"{_STYLES.get(kind, '')}{text}{_RESET}" if _STYLES else text


def say(message):
    """Print a Compass reply."""
    print(f"{color('bot', '[Compass]')} {message}")
