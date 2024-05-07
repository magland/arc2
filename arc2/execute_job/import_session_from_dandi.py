import lindi  # noqa: F401
from ..dj_init.dj_init import SPYGLASS_BASE_DIR

import tempfile

import requests
import spyglass.data_import as sdi  # noqa: E402
import spyglass.common as sgc

import dendro.client as dc


def import_session_from_dandi(
    *,
    dendro_project_id: str,
    nwb_file_id: str,
    dandiset_id: str,
    dandiset_version: str,
    nwb_file_path: str,
    nwb_file_url: str,
):
    fname = f'{SPYGLASS_BASE_DIR}/raw/{nwb_file_id}.nwb.lindi.json'
    name_adj = f'{nwb_file_id}_.nwb.lindi.json'
    lindi_file_url = _create_lindi_file(hdf5_url=nwb_file_url, dendro_project_id=dendro_project_id)
    _download_file(output_fname=fname, url=lindi_file_url)
    sdi.insert_sessions(f'{nwb_file_id}.nwb.lindi.json')
    for row in (sgc.Nwbfile & {'nwb_file_name': name_adj}):
        row['nwb_file_url'] = lindi_file_url
        row['nwb_file_description'] = f'{dandiset_id}/{dandiset_version}/{nwb_file_path}'
        sgc.Nwbfile().update1(row)


def _create_lindi_file(*, hdf5_url: str, dendro_project_id: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        f = lindi.LindiH5pyFile.from_hdf5_file(
            hdf5_url,
            zarr_store_opts=lindi.LindiH5ZarrStoreOpts(
                num_dataset_chunks_threshold=5000
            ),
            local_cache=lindi.LocalCache(cache_dir='lindi_cache')
        )
        tmp_lindi_fname = f'{tmpdir}/file.lindi.json'
        f.write_lindi_file(tmp_lindi_fname)
        return dc.upload_file_blob(
            project_id=dendro_project_id,
            file_name=tmp_lindi_fname
        )


def _download_file(*, output_fname: str, url: str):
    print(f'Downloading {url} to {output_fname}')
    r = requests.get(url)
    with open(output_fname, 'wb') as f:
        f.write(r.content)
