from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input


class StringLoader(Screen):
    BINDINGS = [("enter", "app.pop_screen")]

    def compose(self) -> ComposeResult:
        yield Static(" Open From String ", id="title")
        yield Static("Enter a string to load a dataset from:", id="prompt")
        yield Input("", id="string-to-load")
        yield Static("Press any key to continue [blink]_[/]", id="any-key")

    @on(Input.Submitted, "#string-to-load")
    def submit_input(self, message: Input.Submitted) -> None:
        self.dismiss(message.value or None)
