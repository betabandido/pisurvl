from pisurvl.exceptions import UnknownCommandException


class RequestProcessor:
    def __init__(self, surveillance_manager, response_processor):
        self._surveillance_manager = surveillance_manager
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
            raise UnknownCommandException('Unknown command: {}'.format(request['cmd']))

        handler(request)

    def _process_peek(self, request):
        self._surveillance_manager.queue_surveillance_request(
            request,
            self._process_response
        )

    def _process_state_query(self, request):
        self._process_response(
            request,
            {'enabled': self._surveillance_manager.is_surveillance_enabled()}
        )

    def _process_enable(self, request):
        self._surveillance_manager.start_surveillance()
        self._process_state_query(request)

    def _process_disable(self, request):
        self._surveillance_manager.stop_surveillance()
        self._process_state_query(request)

    def _process_response(self, request, response):
        common_fields = {
            'id': request['id'],
            'cmd': request['cmd']
        }
        response = {**common_fields, **response}
        self._response_processor.process(response)
