from pathlib import Path


def remove_file(location: str | Path):
    path = Path(location)
    if path.exists():
        path.unlink()
    else:
        pass


def remove_dir(location: str | Path):
    path = Path(location)
    if path.exists():
        path.rmdir()
    else:
        pass
