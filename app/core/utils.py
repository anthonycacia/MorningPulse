from typing import List

def chunk_list(items: List[str], size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]