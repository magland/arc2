import os
import yaml
import shutil
import traceback
import sys


def execute_job(*, job_id: str):
    from ..engine.engine import _add
    queued_dirname = f'jobs/queued/{job_id}'
    running_dirname = f'jobs/running/{job_id}'
    completed_dirname = f'jobs/completed/{job_id}'
    failed_dirname = f'jobs/failed/{job_id}'
    job_fname = f'{queued_dirname}/job.yaml'
    if not os.path.exists(job_fname):
        raise Exception(f'Job file not found: {job_fname}')
    _move_dir(src=queued_dirname, dst=running_dirname)
    _add(files=f'{queued_dirname} {running_dirname}', message=f'RUN {job_id}')
    job_fname = f'{running_dirname}/job.yaml'
    try:
        with open(job_fname) as f:
            job = yaml.safe_load(f)
        job_type = job['type']
        job_params = job.get('params', {})
        with capture_console_output(f'{running_dirname}/console_output.txt'):
            execute_job_helper(job_type=job_type, job_params=job_params)
        _move_dir(src=running_dirname, dst=completed_dirname)
        _add(files=f'{running_dirname} {completed_dirname}', message=f'COMPLETE {job_id}')
    except Exception:
        _move_dir(src=running_dirname, dst=failed_dirname)
        error_fname = f'{failed_dirname}/error.txt'
        # write traceback to error_fname
        with open(error_fname, 'w') as f:
            f.write(traceback.format_exc())
        _add(files=f'{running_dirname} {failed_dirname}', message=f'FAIL {job_id}')
        raise


def _move_dir(src: str, dst: str):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)


def execute_job_helper(*, job_type: str, job_params: dict):
    if job_type == 'echo':
        message = job_params['message']
        print(message)
    elif job_type == 'import_session_from_dandi':
        from .. import dj_init  # noqa: F401
        from .import_session_from_dandi import import_session_from_dandi
        nwb_file_id = job_params['nwb_file_id']
        dandiset_id = job_params['dandiset_id']
        dandiset_version = job_params['dandiset_version']
        nwb_file_path = job_params['nwb_file_path']
        nwb_file_url = job_params['nwb_file_url']
        import_session_from_dandi(
            nwb_file_id=nwb_file_id,
            dandiset_id=dandiset_id,
            dandiset_version=dandiset_version,
            nwb_file_path=nwb_file_path,
            nwb_file_url=nwb_file_url,
        )
    else:
        raise Exception(f'Unknown job type: {job_type}')


def capture_console_output(fname):
    class ConsoleOutput:
        def __enter__(self):
            self.stdout = sys.stdout
            self.stderr = sys.stderr
            self.file = open(fname, 'w')
            sys.stdout = self.file
            sys.stderr = self.file
            return self

        def __exit__(self, exc_type, exc_value, tb):
            sys.stdout = self.stdout
            sys.stderr = self.stderr
            self.file.close()

    return ConsoleOutput()
