"""Main module."""

import sys
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Label, Pretty
from textual.reactive import reactive
from textual_fspicker import FileOpen, Filters
import yt.utilities
from .widgets import DatasetTree
import yt
from yt.data_objects.static_output import Dataset


class YTExplorerApp(App):
    """An app to explore datasets with yt"""

    BINDINGS = [("q", "quit"), ("o", "open_button")]

    dataset: reactive[Dataset | None] = reactive(None)

    def __init__(self, path="./") -> None:
        self.path = path
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the layout."""
        yield Header()
        yield Footer()
        yield Label(f"Opened file: {self.dataset or 'None'}")
        yield ScrollableContainer(DatasetTree("hi"))
        yield Pretty(getattr(self.dataset, "parameters", {}))

    def action_open_button(self) -> None:
        """Open a dataset."""
        self.push_screen(
            FileOpen(
                ".",
                filters=Filters(
                    ("Any", lambda _: True),
                    ("Enzo", lambda p: p.suffix.lower() == ".hierarchy"),
                    (
                        "RAMSES",
                        lambda p: str(p).startswith("info_")
                        and p.suffix.lower() == ".txt",
                    ),
                ),
            ),
            callback=self.open_file,
        )

    def open_file(self, to_show: Path | None) -> None:
        new_label = "Opened file"
        try:
            self.dataset = yt.load(to_show)
        except FileNotFoundError as exc:
            new_label = "File not found"
        except yt.utilities.exceptions.YTUnidentifiedDataType as exc:
            new_label = "Could not identify as a yt dataset."
        except yt.utilities.exceptions.YTAmbiguousDataType as exc:
            new_label = "Ambiguous dataset."
        else:
            new_label = f"Opened file: {to_show}"
        self.query_one(Label).update(new_label)

    def action_quit(self) -> None:
        """Quit the app."""
        sys.exit()
