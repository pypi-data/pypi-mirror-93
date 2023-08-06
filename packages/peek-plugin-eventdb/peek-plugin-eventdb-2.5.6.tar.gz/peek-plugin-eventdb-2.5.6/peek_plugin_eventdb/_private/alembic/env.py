from peek_plugin_base.storage.AlembicEnvBase import AlembicEnvBase

from peek_plugin_eventdb._private.storage import DeclarativeBase
from peek_plugin_eventdb._private.storage.DeclarativeBase import loadStorageTuples

loadStorageTuples()

alembicEnv = AlembicEnvBase(DeclarativeBase.DeclarativeBase.metadata)
alembicEnv.run()