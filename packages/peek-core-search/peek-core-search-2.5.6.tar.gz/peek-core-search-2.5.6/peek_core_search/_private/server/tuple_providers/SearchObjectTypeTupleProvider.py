import logging
from typing import Union

from twisted.internet.defer import Deferred

from peek_core_search._private.storage.SearchObjectTypeTuple import \
    SearchObjectTypeTuple
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

logger = logging.getLogger(__name__)


class SearchObjectTypeTupleProvider(TuplesProviderABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    @deferToThreadWrapWithLogger(logger)
    def makeVortexMsg(self, filt: dict,
                      tupleSelector: TupleSelector) -> Union[Deferred, bytes]:

        session = self._ormSessionCreator()
        try:
            tuples = (
                session
                    .query(SearchObjectTypeTuple)
                    .order_by(SearchObjectTypeTuple.order, SearchObjectTypeTuple.title)
                    .all()
            )

            # Create the vortex message
            return Payload(filt, tuples=tuples).makePayloadEnvelope().toVortexMsg()

        finally:
            session.close()
