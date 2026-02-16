def progress_bar(time_left: int, total: int, size: int = 10) -> str:
    from math import floor
    ratio = time_left / total
    filled = floor(ratio * size)
    empty = size - filled
    return "█" * filled + "░" * empty
