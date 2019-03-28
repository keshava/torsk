import click

from torsk.scripts import defaults
from torsk.scripts import scale
from torsk.scripts import animate
from torsk.scripts import ncextract
from torsk.scripts import prediction_performance
from torsk.scripts import detect
from torsk.scripts import detect_row
from torsk.scripts import anomaly_count
from torsk.scripts import cycle_predict


@click.group('torsk')
def cli():
    """torsk command line interface"""
    pass


cli.add_command(defaults.cli)
cli.add_command(scale.cli)
cli.add_command(animate.cli)
cli.add_command(ncextract.cli)
cli.add_command(prediction_performance.cli)
cli.add_command(detect.cli)
cli.add_command(detect_row.cli)
cli.add_command(anomaly_count.cli)
cli.add_command(cycle_predict.cli)


if __name__ == "__main__":
    cli()
