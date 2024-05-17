"""Main module."""

import sys
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer
from .widgets import DatasetTree
import yt


class YTExplorerApp(App):
    """An app to explore datasets with yt"""

    BINDINGS = [("q", "quit")]

    def __init__(self, path="./") -> None:
        self.path = path
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the layout."""
        yield Header()
        yield Footer()
        yield ScrollableContainer(DatasetTree(self.path))

    def action_quit(self) -> None:
        """Quit the app."""
        sys.exit()
