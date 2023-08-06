import logging

from peek_plugin_eventdb._private.storage.EventDBPropertyTable import EventDBPropertyTable
from twisted.internet.defer import Deferred
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

from peek_plugin_base.storage.DbConnection import DbSessionCreator

logger = logging.getLogger(__name__)


class EventDBPropertyTupleProvider(TuplesProviderABC):
    def __init__(self, dbSessionCreator: DbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    @deferToThreadWrapWithLogger(logger)
    def makeVortexMsg(self, filt: dict, tupleSelector: TupleSelector) -> Deferred:
        dbSession = self._dbSessionCreator()
        try:
            tableObs = dbSession.query(EventDBPropertyTable).all()
            tuples = [o.toTuple() for o in tableObs]

        finally:
            dbSession.close()

        payloadEnvelope = Payload(filt=filt, tuples=tuples).makePayloadEnvelope()
        vortexMsg = payloadEnvelope.toVortexMsg()
        return vortexMsg
