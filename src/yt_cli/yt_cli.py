"""Main module."""

import sys
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Header, Footer, Label
from textual.reactive import reactive
from textual_fspicker import FileOpen, Filters
import yt.utilities
from .widgets import GridDisplayTree, GridInfoDisplay
import yt
from yt.data_objects.static_output import Dataset
from .screens import StringLoader


class YTExplorerApp(App):
    """An app to explore datasets with yt"""

    SCREENS = {"string_loader": StringLoader()}
    BINDINGS = [("q", "quit"), ("o", "open_button"), ("ctrl+o", "string_loader")]

    dataset: reactive[Dataset | None] = reactive(None)

    def compose(self) -> ComposeResult:
        """Compose the layout."""
        yield Header()
        yield Footer()
        yield Label(f"Opened file: {self.dataset or 'None'}")
        with Horizontal():
            yield ScrollableContainer(
                GridDisplayTree().data_bind(YTExplorerApp.dataset)
            )
            yield GridInfoDisplay()

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

    def action_string_loader(self) -> None:
        self.push_screen("string_loader", callback=self.open_file)

    def open_file(self, to_show: Path | None) -> None:
        if to_show is None:
            return
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
