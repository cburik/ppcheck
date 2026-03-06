from importlib.metadata import version

from ppcheck.cli import PwnedPasswordChecker

__version__ = version("ppcheck")
__all__ = ["PwnedPasswordChecker", "__version__"]
