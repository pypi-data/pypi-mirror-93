import logging

import pykka

from isc_common import Stack, StackElementNotExist

logger = logging.getLogger(__name__)

class Actor(pykka.ThreadingActor):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def on_receive(self, message):
        message.get('function')(message.get('data'))


class Actors(Stack):
    def tell(self, id, message):


        actor_ref = self.find_one(lambda x: x._actor.id == id)
        actor_ref.tell(message=message)

    def push(self, id):

        if not self.exists(lambda x: x._actor.id == id):
            actor_ref = Actor.start(id=id)
            logger.debug(f'started: {actor_ref}')
            super(Actors, self).push(item=actor_ref)

    def stop(self, id):
        try:
            actor_ref = self.find_one(lambda x: x._actor.id == id)
            actor_ref.stop()
            logger.debug(f'stoped: {actor_ref}')
        except StackElementNotExist:
            pass

    def stop_all(self):
        for actor_ref in self.stack:
            actor_ref.stop()
            logger.debug(f'stoped: {actor_ref}')
