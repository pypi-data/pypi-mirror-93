import datetime
import json
from typing import Any, Dict


def apply(hub, event: Dict, ref: str) -> Dict[str, Any]:
    # Make sure the event is a json serializable object
    try:
        event = json.dumps(event, sort_keys=True)
    finally:
        event = json.loads(event)

    return {"data": event, "timestamp": datetime.datetime.now().timestamp(), "ref": ref}
