import json
from ..messages_and_medias.message import Message
from ..inline.inlinequery import InlineQuery
from ..callback.callbackquery import CallbackQuery
from ..polls.poll import Poll
from ..polls.poll_answer import PollAnswer


class Update(object):
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
        update_id = json_obj.get('update_id')
        if json_obj.get('message') is not None:
            message = Message._de_json(dict(json_obj['message']))
        elif json_obj.get('edited_message') is not None:
            message = Message._de_json(dict(json_obj['edited_message']))
        elif json_obj.get('channel_post') is not None:
            message = Message._de_json(dict(json_obj['channel_post']))
        elif json_obj.get('edited_channel_post') is not None:
            message = Message._de_json(dict(json_obj['edited_channel_post']))
        else:
            message = None

        if json_obj.get('inline_query') is not None:
            inline_query = InlineQuery._de_json(dict(json_obj['inline_query']))
        else:
            inline_query = None

        if json_obj.get("callback_query") is not None:
            callback_query = CallbackQuery._de_json(dict(json_obj['callback_query']))
        else:
            callback_query = None

        if json_obj.get("poll") is not None:
            poll = Poll._de_json(dict(json_obj['poll']))
        else:
            poll = None

        if json_obj.get("poll_answer") is not None:
            poll_answer = PollAnswer._de_json(dict(json_obj['poll_answer']))
        else:
            poll_answer = None
        return cls(update_id, message, inline_query, callback_query, poll, poll_answer)

    def __init__(self, update_id, message, inline_query, callback_query, poll, poll_answer):
        self.update_id = update_id
        self.message = message
        self.inline_query = inline_query
        self.callback_query = callback_query
        self.poll = poll
        self.poll_answer = poll_answer

