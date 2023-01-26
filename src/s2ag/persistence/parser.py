import re
from os import PathLike

import dotenv

#  env = "postgres://fred:secret_pw@127.0.0.1/test_db?sslmode=disable

CONNECTION_RE = re.compile('postgres://([^:]*):([^@]*)@([^/]*)/([^?]*)\?')


def get_connection_string(env_variable_name: str, env_file_name: PathLike):
    parsed = parse(dotenv.dotenv_values(env_file_name)[env_variable_name])
    if parsed is not None:
        user, password, host, dbname = parsed
        return f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'"


def parse(env_entry: str):
    result = None
    match = CONNECTION_RE.search(env_entry)
    if match is not None:
        result = (match.group(1),
                 match.group(2),
                 match.group(3),
                 match.group(4)
        )
    return result
