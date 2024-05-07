import click

@click.group()
def cli():
    pass

@click.command()
def engine():
    from .engine.engine import engine
    engine()

@click.command()
def prepare_spyndle():
    from .prepare_spyndle.prepare_spyndle import prepare_spyndle
    prepare_spyndle()

@click.command()
@click.option('--job-id', required=True, type=str)
def execute_job(job_id: str):
    from .execute_job.execute_job import execute_job
    execute_job(job_id=job_id)

cli.add_command(engine)
cli.add_command(execute_job)
cli.add_command(prepare_spyndle)

def main():
    cli()
