import pickle
import base64


def export_session(session_data: dict) -> bytes:
    raw = pickle.dumps(session_data)
    return base64.b64encode(raw)


def import_session(raw: bytes) -> dict:
    decoded = base64.b64decode(raw)
    return pickle.loads(decoded)
