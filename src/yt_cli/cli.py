"""Console script for yt_cli."""

import yt
import yt_cli

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for yt_cli."""
    console.print("Replace this message by putting your code into " "yt_cli.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")


@app.command()
def info(
    filename: str,
    verbose: bool = False,
    params: bool = False,
    fields: bool = False,
    derived_fields: bool = False,
):
    """Get info about the dataset"""
    if verbose:
        params = fields = derived_fields = True
    ds = yt.load(filename)
    if any([params, fields, derived_fields]):
        ds.index
    console.print(ds)
    console.print("[bold]Dataset Statistics[/bold]")
    console.print()
    console.print(
        f"[bold]Domain Dimensions[/bold]: {ds.domain_dimensions[0]} x {ds.domain_dimensions[1]} x {ds.domain_dimensions[2]}"
    )
    console.print(f"[bold]Domain Left Edge[/bold]: {ds.domain_left_edge}")
    console.print(f"[bold]Domain Right Edge[/bold]: {ds.domain_right_edge}")
    console.print(f"[bold]Current Time[/bold]: {ds.current_time}")
    console.print(f"[bold]Current Redshift[/bold]: {ds.current_redshift}")
    console.print(f"[bold]Cosmological Simulation[/bold]: {ds.cosmological_simulation}")
    if params:
        console.print()
        console.print("[bold]Parameters[/bold]:")
        console.print(ds.parameters)
    if fields:
        console.print()
        console.print("[bold]Fields[/bold]:")
        console.print(ds.field_list)
    if derived_fields:
        console.print()
        console.print("[bold]Derived Fields[/bold]:")
        console.print(ds.derived_field_list)


if __name__ == "__main__":
    app()
