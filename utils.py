from rich.console import Console

console = Console()

def create_block_bar(usage, total_blocks=30, color="green", empty_color="grey37"):
    blocks = int((usage / 100) * total_blocks)
    filled_bar = f"[{color}]" + "█" * blocks + "[/]"
    empty_bar = f"[{empty_color}]" + "█" * (total_blocks - blocks) + "[/]"
    return filled_bar + empty_bar
