from peek_plugin_livedb._private.server.LiveDBReadApi import LiveDBReadApi
from peek_plugin_livedb._private.server.LiveDBWriteApi import LiveDBWriteApi
from peek_plugin_livedb._private.server.controller.LiveDbController import \
    LiveDbController
from peek_plugin_livedb._private.server.controller.LiveDbImportController import \
    LiveDbImportController
from peek_plugin_livedb._private.server.controller.LiveDbValueUpdateQueueController import \
    LiveDbValueUpdateQueueController
from peek_plugin_livedb.server.LiveDBApiABC import LiveDBApiABC
from peek_plugin_livedb.server.LiveDBReadApiABC import LiveDBReadApiABC
from peek_plugin_livedb.server.LiveDBWriteApiABC import LiveDBWriteApiABC


class LiveDBApi(LiveDBApiABC):

    def __init__(self):
        self._readApi = LiveDBReadApi()
        self._writeApi = LiveDBWriteApi()

    def setup(self, queueController: LiveDbValueUpdateQueueController,
              liveDbController: LiveDbController,
              liveDbImportController: LiveDbImportController,
              dbSessionCreator,
              dbEngine):
        self._readApi.setup(liveDbController=liveDbController,
                            dbSessionCreator=dbSessionCreator,
                            dbEngine=dbEngine)

        self._writeApi.setup(queueController=queueController,
                             liveDbController=liveDbController,
                             liveDbImportController=liveDbImportController,
                             readApi=self._readApi,
                             dbSessionCreator=dbSessionCreator,
                             dbEngine=dbEngine)

    def shutdown(self):
        self._readApi.shutdown()
        self._writeApi.shutdown()

        self._readApi = None
        self._writeApi = None

    @property
    def writeApi(self) -> LiveDBWriteApiABC:
        return self._writeApi

    @property
    def readApi(self) -> LiveDBReadApiABC:
        return self._readApi
