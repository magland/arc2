from typing import Dict, Any
import os
import tempfile
import datetime
import subprocess


def engine():
    _pull()
    if not os.path.exists('jobs/submitted'):
        os.makedirs('jobs/submitted')
    for submitted_job_name in os.listdir('jobs/submitted'):
        if submitted_job_name.endswith('.yaml'):
            # job_id is the file name without the extension
            job_id_desc = submitted_job_name[:-len('.yaml')]
            rndstr = _create_random_string()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            job_id = f'{timestamp}_{rndstr}_{job_id_desc}'
            try:
                _handle_submitted_job(submitted_job_id_desc=job_id_desc, submitted_job_id=job_id)
            except Exception as e:
                print(f'Error handling job {job_id}: {e}')
                continue


def _handle_submitted_job(submitted_job_id_desc: str, submitted_job_id: str):
    submitted_job_fname = f'jobs/submitted/{submitted_job_id_desc}.yaml'
    queued_dirname = f'jobs/queued/{submitted_job_id}'
    os.makedirs(queued_dirname)
    queued_job_fname = f'{queued_dirname}/job.yaml'
    _move_file(submitted_job_fname, queued_job_fname)
    _add(files=f'{submitted_job_fname} {queued_job_fname}', message=f'QUEUE {submitted_job_id}')
    _launch_detached_process(cmd=f'arc2 execute-job --job-id {submitted_job_id}', env={}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _move_file(src: str, dst: str):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    os.rename(src, dst)


def _add(*, files: str, message: str):
    _append_to_log(message=message)
    _run_shell_script(f'git add {files} && git commit -m "{message}"')
    _run_shell_script('git push')


def _append_to_log(*, message: str):
    log_fname = 'jobs/log.txt'
    with open(log_fname, 'a') as f:
        f.write(f'{datetime.datetime.now()} {message}\n')


def _pull():
    _run_shell_script('git pull')


def _run_shell_script(script):
    with tempfile.TemporaryDirectory() as tmpdir:
        script_fname = f'{tmpdir}/script.sh'
        with open(script_fname, 'w') as f:
            f.write(script)
        os.system(f'bash {script_fname}')


def _launch_detached_process(*, cmd: str, env: Dict[str, str], stdout: Any, stderr: Any):
    subprocess.Popen(
        cmd.split(' '),
        env={
            **os.environ.copy(),
            **env
        },
        stdout=stdout,
        stderr=stderr,
        start_new_session=True
    )


def _create_random_string():
    return os.urandom(4).hex()


if __name__ == "__main__":
    engine()
