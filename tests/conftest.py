"""Windows compatibility for gltest's temporary stdin cleanup."""
import os

_unlink = os.unlink

def _unlink_for_gltest(path, *args, **kwargs):
    try:
        return _unlink(path, *args, **kwargs)
    except PermissionError as exc:
        if getattr(exc, "winerror", None) == 32 and os.path.basename(str(path)).lower().startswith("tmp"):
            return None
        raise

os.unlink = _unlink_for_gltest
