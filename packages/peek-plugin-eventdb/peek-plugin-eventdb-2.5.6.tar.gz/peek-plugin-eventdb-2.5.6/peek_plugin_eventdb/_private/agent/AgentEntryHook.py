import logging

from peek_plugin_base.agent.PluginAgentEntryHookABC import PluginAgentEntryHookABC
from peek_plugin_eventdb.tuples import loadPublicTuples

logger = logging.getLogger(__name__)


class AgentEntryHook(PluginAgentEntryHookABC):

    def load(self) -> None:
        # loadStorageTuples()
        # loadPrivateTuples()
        loadPublicTuples()

        logger.debug("Loaded")

    def start(self):
        logger.debug("Started")

    def stop(self):
        logger.debug("Stopped")

    def unload(self):
        logger.debug("Unloaded")
