"""Console script for yt_cli."""

import yt
from .yt_cli import YTExplorerApp
import numpy as np

import typer
from rich.console import Console
from typing_extensions import Annotated
from typing import List, Optional, Union

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


@app.command()
def stats(
    filename: str,
    fields: Annotated[
        Optional[List[str]], typer.Argument(help="fields to get statistics for")
    ] = None,
    field_type: Optional[str] = "gas",
):
    """Get statistics about the dataset"""
    if fields is None or len(fields) == 0:
        fields = ["density", "temperature"]
    ds = yt.load(filename)
    dd = ds.all_data()
    field_requests = [(field_type, field) for field in fields]
    mi = np.atleast_1d(dd.min(field_requests))
    ma = np.atleast_1d(dd.max(field_requests))
    means_vol = np.atleast_1d(dd.mean(field_requests, weight="volume"))
    means_mass = np.atleast_1d(dd.mean(field_requests, weight="mass"))
    console.print(f"[bold]Statistics for {filename}[/bold]")
    for min_val, max_val, mean_vol, mean_mass, field in zip(
        mi, ma, means_vol, means_mass, fields
    ):
        console.print(f"[bold]{field_type}, {field}[/bold]:")
        console.print(f"Min: {min_val}")
        console.print(f"Max: {max_val}")
        console.print(f"Mean (volume-weighted): {mean_vol}")
        console.print(f"Mean (mass-weighted): {mean_mass}")
        console.print()


@app.command()
def slice(
    filename: str,
    field: str,
    field_type: Optional[str] = "gas",
    width: Optional[float] = 1.0,
    center: Optional[List[float]] = [0.5, 0.5, 0.5],
    cmap: Optional[str] = "viridis",
    output: Optional[str] = None,
    axis: Optional[str] = "z",
):
    """Plot a slice of the dataset"""
    ds = yt.load(filename)
    slc = yt.SlicePlot(
        ds, axis, (field_type, field), center=center, width=(width, "unitary")
    )
    slc.set_cmap(field, cmap)
    slc.save(output)


@app.command()
def project(
    filename: str,
    field: str,
    field_type: Optional[str] = "gas",
    width: Optional[float] = 1.0,
    center: Optional[List[float]] = [0.5, 0.5, 0.5],
    cmap: Optional[str] = "viridis",
    output: Optional[str] = None,
    axis: Optional[str] = "z",
    weight_field: Optional[str] = None,
):
    """Plot a projection of the dataset"""
    ds = yt.load(filename)
    prj = yt.ProjectionPlot(
        ds,
        axis,
        (field_type, field),
        weight_field=weight_field,
        center=center,
        width=(width, "unitary"),
    )
    prj.set_cmap(field, cmap)
    prj.save(output)


@app.command()
def pdf(
    filename: str,
    field: str,
    field_type: Optional[str] = "gas",
    bins: Optional[int] = 64,
    output: Optional[str] = None,
):
    """Plot a probability distribution function of the dataset"""
    ds = yt.load(filename)
    dd = ds.all_data()
    field = (field_type, field)
    y_field = (field_type, "cell_volume")
    hist = yt.create_profile(dd, field, y_field, n_bins=bins, fractional=True)
    hist.plot().save(output)


@app.command()
def profile(
    filename: str,
    x_field: str = "density",
    field_type: Optional[str] = "gas",
    weight_field: Optional[str] = None,
    output: Optional[str] = None,
    y_fields: Annotated[
        Optional[List[str]], typer.Argument(help="fields to profile")
    ] = None,
):
    """Plot a profile of the dataset"""
    ds = yt.load(filename)
    if y_fields is None or len(y_fields) == 0:
        y_fields = ["volume"]
    dd = ds.all_data()
    x_field = (field_type, x_field)
    y_fields = [(field_type, field) for field in y_fields]
    prof = yt.ProfilePlot(
        dd,
        x_field,
        y_fields,
        weight_field=weight_field,
    )
    prof.save(output)


@app.command()
def run(
    path: Optional[str] = "./",
):
    """Run the yt explorer app"""
    YTExplorerApp().run()


if __name__ == "__main__":
    app()
