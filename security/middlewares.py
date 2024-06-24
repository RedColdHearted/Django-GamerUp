class RemoveServerHeaderMiddleware:
    """
    remove security header from responses for better web server safety
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.__setitem__('Server', 'lol')
        return response
