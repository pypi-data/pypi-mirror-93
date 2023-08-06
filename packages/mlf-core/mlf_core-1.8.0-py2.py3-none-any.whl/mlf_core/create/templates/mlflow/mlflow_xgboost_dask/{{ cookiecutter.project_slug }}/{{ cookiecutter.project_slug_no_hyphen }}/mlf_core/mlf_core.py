import tempfile
import mlflow
import subprocess
import os
import numpy as np
import random
from rich import print


def set_general_random_seeds(seed):
    os.environ['PYTHONHASHSEED'] = str(seed)  # Python general
    np.random.seed(seed)  # Numpy random
    random.seed(seed)  # Python random


def log_sys_intel_conda_env():
    reports_output_dir = tempfile.mkdtemp()
    log_system_intelligence(reports_output_dir)
    log_conda_environment(reports_output_dir)


def log_system_intelligence(reports_output_dir: str):
    # Scoped import to prevent issues like RuntimeError: Numba cannot operate on non-primary CUDA context
    from system_intelligence.query import query_and_export

    print(f'[bold blue]Writing reports locally to {reports_output_dir}\n')
    print('[bold blue]Running system-intelligence')
    query_and_export(query_scope={'all'},
                     verbose=False,
                     export_format='json',
                     generate_html_table=True,
                     output=f'{reports_output_dir}/system_intelligence.json')
    print('[bold blue]Uploading system-intelligence report as a run artifact...')
    mlflow.log_artifacts(reports_output_dir, artifact_path='reports')


def log_conda_environment(reports_output_dir: str):
    print('[bold blue]Exporting conda environment...')
    conda_env_filehandler = open(f'{reports_output_dir}/{{ cookiecutter.project_slug_no_hyphen }}_conda_environment.yml', "w")
    subprocess.call(['conda', 'env', 'export', '--name', '{{ cookiecutter.project_slug_no_hyphen }}'], stdout=conda_env_filehandler)
    print('[bold blue]Uploading conda environment report as a run artifact...')
    mlflow.log_artifact(f'{reports_output_dir}/{{ cookiecutter.project_slug_no_hyphen }}_conda_environment.yml', artifact_path='reports')
