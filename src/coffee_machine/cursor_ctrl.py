def move_cursor_up() -> str:
    return "\033[A"


def clear_screen() -> None:
    print("\033[2J\033[H", end="")
