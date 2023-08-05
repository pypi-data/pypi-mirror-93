import click
import rifl

@click.command()
@click.argument('analysis-params-file', type=click.Path(exists=True))
def _analyze(analysis_params_file):
    rifl.analyze(analysis_params_file)
