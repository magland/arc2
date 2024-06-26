import os
import yaml

# It's important to configure datajoint before importing spyglass
import datajoint as dj

config_fname = 'arc2.yaml'
if not os.path.exists(config_fname):
    raise Exception(f'Config file not found: {config_fname}')
with open(config_fname, 'r') as f:
    config = yaml.safe_load(f)

SPYGLASS_INSTANCE = config.get("spyglass_instance", None)
if SPYGLASS_INSTANCE is None:
    raise Exception("Please set spyglass_instance in the config file")

DENDRO_PROJECT_ID = config.get("dendro_project_id", None)
if DENDRO_PROJECT_ID is None:
    raise Exception("Please set dendro_project_id in the config file")

if SPYGLASS_INSTANCE == "franklab":
    DJ_DATABASE_HOST = os.environ.get("DJ_DATABASE_HOST_FRANKLAB", None)
    if DJ_DATABASE_HOST is None:
        raise Exception("Please set DJ_DATABASE_HOST_FRANKLAB environment variable")
    DJ_DATABASE_USER = os.environ.get("DJ_DATABASE_USER_FRANKLAB", None)
    if DJ_DATABASE_USER is None:
        raise Exception("Please set DJ_DATABASE_USER_FRANKLAB environment variable")
    DJ_DATABASE_PASSWORD = os.environ.get("DJ_DATABASE_PASSWORD_FRANKLAB", None)
    if DJ_DATABASE_PASSWORD is None:
        raise Exception("Please set DJ_DATABASE_PASSWORD_FRANKLAB environment variable")
elif SPYGLASS_INSTANCE == "arc-dev":
    DJ_DATABASE_HOST = os.environ.get("DJ_DATABASE_HOST_ARC_DEV", None)
    if DJ_DATABASE_HOST is None:
        raise Exception("Please set DJ_DATABASE_HOST_ARC_DEV environment variable")
    DJ_DATABASE_USER = os.environ.get("DJ_DATABASE_USER_ARC_DEV", None)
    if DJ_DATABASE_USER is None:
        raise Exception("Please set DJ_DATABASE_USER_ARC_DEV environment variable")
    DJ_DATABASE_PASSWORD = os.environ.get("DJ_DATABASE_PASSWORD_ARC_DEV", None)
    if DJ_DATABASE_PASSWORD is None:
        raise Exception("Please set DJ_DATABASE_PASSWORD_ARC_DEV environment variable")
else:
    raise Exception(f"Unknown SPYGLASS_INSTANCE: {SPYGLASS_INSTANCE}")

working_dir = os.getcwd()
SPYGLASS_BASE_DIR = f'{working_dir}/spyglass_data'

dj.config['database.host'] = DJ_DATABASE_HOST
dj.config['database.user'] = DJ_DATABASE_USER
dj.config['database.password'] = DJ_DATABASE_PASSWORD

dj.config['stores'] = {
    'raw': {
        'protocol': 'file',
        'location': f'{SPYGLASS_BASE_DIR}/raw',
        'stage': f'{SPYGLASS_BASE_DIR}/raw'
    },
    'analysis': {
        'protocol': 'file',
        'location': f'{SPYGLASS_BASE_DIR}/analysis',
        'stage': f'{SPYGLASS_BASE_DIR}/analysis',
    }
}
dj.config['custom'] = {
    "spyglass_dirs": {
        "base": SPYGLASS_BASE_DIR,
        "raw": f"{SPYGLASS_BASE_DIR}/raw",
        "analysis": f"{SPYGLASS_BASE_DIR}/analysis",
        "recording": f"{SPYGLASS_BASE_DIR}/recording",
        "sorting": f"{SPYGLASS_BASE_DIR}/spikesorting",
        "waveforms": f"{SPYGLASS_BASE_DIR}/waveforms",
        "temp": f"{SPYGLASS_BASE_DIR}/tmp",
        "video": f"{SPYGLASS_BASE_DIR}/video"
    },
    "kachery_dirs": {
        "cloud": f"{SPYGLASS_BASE_DIR}/.kachery-cloud",
        "storage": f"{SPYGLASS_BASE_DIR}/kachery_storage",
        "temp": f"{SPYGLASS_BASE_DIR}/tmp"
    },
    "dlc_dirs": {
        "base": f"{SPYGLASS_BASE_DIR}/deeplabcut",
        "project": f"{SPYGLASS_BASE_DIR}/deeplabcut/projects",
        "video": f"{SPYGLASS_BASE_DIR}/deeplabcut/video",
        "output": f"{SPYGLASS_BASE_DIR}/deeplabcut/output"
    },
    "kachery_zone": "default"
}

LINDI_LOCAL_CACHE_DIR = f'{SPYGLASS_BASE_DIR}/lindi_cache'
if not os.path.exists(LINDI_LOCAL_CACHE_DIR):
    os.makedirs(LINDI_LOCAL_CACHE_DIR)
os.environ['LINDI_LOCAL_CACHE_DIR'] = LINDI_LOCAL_CACHE_DIR

# create directories if they don't exist
if not os.path.exists(f'{SPYGLASS_BASE_DIR}/raw'):
    os.makedirs(f'{SPYGLASS_BASE_DIR}/raw')
if not os.path.exists(f'{SPYGLASS_BASE_DIR}/analysis'):
    os.makedirs(f'{SPYGLASS_BASE_DIR}/analysis')

os.environ['DJ_SUPPORT_FILEPATH_MANAGEMENT'] = 'TRUE'
