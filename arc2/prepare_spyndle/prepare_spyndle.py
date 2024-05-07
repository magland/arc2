import tempfile


def prepare_spyndle():
    from .. import dj_init  # noqa: F401
    from .create_table_names import create_table_names
    from .prepare_session_files import prepare_sessions, upload_session_files, prepare_tables
    with tempfile.TemporaryDirectory() as tmpdir:
        create_table_names(tmpdir)
        prepare_tables(tmpdir)
        prepare_sessions(tmpdir)
        upload_session_files(tmpdir)
