from textual.widgets import Static
from textual.reactive import reactive
from yt.data_objects.index_subobjects.grid_patch import AMRGridPatch


class GridInfoDisplay(Static):
    grid: reactive[AMRGridPatch | None] = reactive(None)

    def compose(self):
        yield Static(id="grid_info")
        yield Static(id="grid_view")

    def watch_grid(self, grid: AMRGridPatch) -> None:
        if grid is None:
            return
        grid_info: Static = self.query_one("#grid_info")
        grid_info.update(
            f"Left Edge: {grid.LeftEdge}\n"
            f"Right Edge: {grid.RightEdge}\n"
            f"Active Dimensions: {grid.ActiveDimensions}\n"
            f"Level: {grid.Level}\n"
        )
