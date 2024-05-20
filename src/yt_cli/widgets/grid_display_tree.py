from textual.app import ComposeResult
from textual.widgets import Tree, Static
from textual.reactive import reactive
from yt.data_objects.static_output import Dataset


class GridDisplayTree(Static):
    dataset: reactive[Dataset | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield Tree(label="Grid Hierarchy", id="grid_hierarchy")

    def watch_dataset(self, dataset: Dataset) -> None:
        if dataset is None:
            return
        if not hasattr(dataset.index, "grids"):
            return

        def dictify(g):
            return {
                "ActiveDimensions": g.ActiveDimensions,
                "LeftEdge": g.LeftEdge,
                "RightEdge": g.RightEdge,
                "Level": g.Level,
                "grid": g,
            }

        tree: Tree[dict] = self.query_one(Tree)
        tree.root.expand()

        def add_children(node, g):
            data = dictify(g)
            if len(g.Children) == 0:
                node.add_leaf(str(g), data=data)
            else:
                n = node.add(str(g), data=data)
                for c in g.Children:
                    add_children(n, c)

        for grid in dataset.index.select_grids(0):
            # These are all the root grids
            node = tree.root.add(str(grid), data=dictify(grid), expand=True)
            for c in grid.Children:
                add_children(node, c)
