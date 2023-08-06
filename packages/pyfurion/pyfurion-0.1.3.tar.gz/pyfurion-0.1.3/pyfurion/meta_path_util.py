import re


def toPath(env,  namespace,  group_key,  meta_key):
    return f'/{namespace}/{env}/{group_key}/{meta_key}'


def group(env,  namespace,  group_key):
    return f'/{namespace}/{env}/{group_key}'


def toKey(meta_path: str):
    if not meta_path:
        return None
    return meta_path[meta_path.rindex('/')+1:]


def toNamespace(metaPath: str):
    if not metaPath:
        return None
    namespace = re.findall(r'^/([^/]+)/', metaPath)
    return namespace[0] if namespace else ''


def toGroup(metaPath: str):
    if not metaPath:
        return None
    metaPath = metaPath[:metaPath.rindex('/')]
    return metaPath[metaPath.rindex('/')+1:]
