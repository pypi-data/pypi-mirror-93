class SecurityHeaderMiddleware(object):
    """
    Add security headers to all responses
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response["Cache-Control"] = "no-cache, no-store"
        response["X-Content-Type-Options"] = "nosniff"
        response["X-XSS-Protection"] = "1; mode=block"

        return response
