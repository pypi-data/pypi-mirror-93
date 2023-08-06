import json
from ..users_and_chats.user import User


class InlineQuery(object):
    @classmethod
    def _de_json(cls, json_str):
        if json_str is None:
            return None
        if isinstance(json_str, dict):
            json_obj = json_str
        elif isinstance(json_str, str):
            json_obj = json.loads(json_str)
        else:
            raise ValueError("Expected dict or str type")

        id = json_obj.get("id")
        from_user = User._de_json(dict(json_obj.get("from")))
        query = json_obj.get("query")
        offset = json_obj.get("offset")
        return cls(id, from_user, query, offset)

    def __init__(self, id, from_user, query, offset):
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset
