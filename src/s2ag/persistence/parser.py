import re

#  env = "postgres://fred:secret_pw@127.0.0.1/test_db?sslmode=disable

CONNECTION_RE = re.compile('postgres://([^:]*):([^@]*)@([^/]*)/([^?]*)\?')


def parse(env_entry: str):
    result = {}
    match = CONNECTION_RE.search(env_entry)
    if match is not None:
        result['user'] = match.group(1)
        result['password'] = match.group(2)
        result['host'] = match.group(3)
        result['dbname'] = match.group(4)
    return result
