#!/usr/bin/env python3

import os

from dotenv import load_dotenv


def load_env_var(filepath: str) -> str:
    projectroot = os.path.dirname(os.path.dirname(os.path.realpath(filepath)))

    dotenv_path = os.path.join(projectroot, '.env')
    load_dotenv(dotenv_path)
    envtype = os.environ.get('ENV_TYPE', default='local')
    load_dotenv(dotenv_path + '.' + envtype)

    return projectroot
