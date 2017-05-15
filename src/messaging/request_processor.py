class RequestProcessor:
    def __init__(self, app, response_processor):
        self._app = app
        self._response_processor = response_processor
        self._command_handlers = {
            'peek':         self._process_peek,
            'query-state':  self._process_state_query,
            'enable':       self._process_enable,
            'disable':      self._process_disable
        }

    def process(self, request):
        print('Request: {}'.format(request))

        handler = self._command_handlers.get(request['cmd'], None)
        if handler is None:
            # TODO: send a warning email?
            print('Unknown command: {}'.format(request['cmd']))
            return

        handler(request)

    def _process_peek(self, request):
        self._app.queue_surveillance_request(
            request,
            self._process_response)

    def _process_state_query(self, request):
        self._process_response(request, {'enabled': self._app.is_surveillance_enabled()})

    def _process_enable(self, request):
        self._app.start_surveillance()
        self._process_state_query(request)

    def _process_disable(self, request):
        self._app.stop_surveillance()
        self._process_state_query(request)

    def _process_response(self, request, response):
        common_fields = {
            'id': request['id'],
            'cmd': request['cmd']
        }
        response = {**common_fields, **response}
        self._response_processor.process(response)
