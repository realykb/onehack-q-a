import json
import falcon

from game.game import Game
from .facebook_inbound import FacebookWebHook
from .status import Status
from .voice_answer import Answer
from .event import Event
from .stt import STT

application = falcon.API()


class Index(object):
    @staticmethod
    def on_post(req, resp):

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['body'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

        # Create a JSON representation of the resource
        resp.body = json.dumps(req.context['body'], ensure_ascii=False)

        # The following line can be omitted because 200 is the default
        # status returned by the framework, but it is included here to
        # illustrate how this may be overridden as needed.
        resp.status = falcon.HTTP_200


game = Game()
index = Index()
inbound_message = FacebookWebHook(game)
status = Status()
answer = Answer(game)
event = Event()
stt = STT(game)
application.add_route('/', index)
application.add_route('/status', status)
application.add_route('/inbound', inbound_message)
application.add_route('/answer', answer)
application.add_route('/event', event)
application.add_route('/stt', stt)
