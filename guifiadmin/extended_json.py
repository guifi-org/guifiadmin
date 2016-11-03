#!/usr/bin/env python
import json
from functools import partial


class GuifiAdminJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)


dumps = partial(json.dumps, cls=GuifiAdminJSONEncoder)
