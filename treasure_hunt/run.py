import json

from app import create_app
from werkzeug.exceptions import HTTPException

if __name__ == "__main__":
    app = create_app()

    @app.errorhandler(HTTPException)
    def handle_http_exceptions(err):
        """
        Custom handler for HTTP exceptions.
        Returns JSON output instead of HTML.
        """
        response = err.get_response()
        payload = {
            "status_code": err.code,
            "error": err.name,
            "message": err.description,
        }
        response.data = json.dumps(payload)
        response.content_type = "application/json"
        return response

    app.run(port=8000, debug=True)
