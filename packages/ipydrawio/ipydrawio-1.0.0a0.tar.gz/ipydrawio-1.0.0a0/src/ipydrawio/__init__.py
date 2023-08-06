from pathlib import Path

from ._version import __version__
from .widget_diagram import Diagram


def _jupyter_labextension_paths():
    here = Path(__file__).parent

    return [
        dict(
            src=f"{pkg.parent.relative_to(here).as_posix()}",
            dest=f"{pkg.parent.parent.name}/{pkg.parent.name}",
        )
        for pkg in (here / "labextensions").glob("*/*/package.json")
    ]


__all__ = ["__version__", "_jupyter_labextension_paths", "Diagram"]
