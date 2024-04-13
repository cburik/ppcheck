from pathlib import Path


def remove_file(location: str):
    path = Path(location)
    if path.exists():
        path.unlink()
    else:
        pass
