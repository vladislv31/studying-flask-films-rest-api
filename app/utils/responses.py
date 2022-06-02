

def successful_response_message(message):
    return {"message": str(message)}, 200


def bad_request_response_message(message):
    return {"message": str(message)}, 400


def unauthorized_request_response_message(message="Access denied."):
    return {"message": str(message)}, 401


def not_found_request_response_message(message):
    return {"message": str(message)}, 404

def internal_server_response_message(message="Internal server error."):
    return {"message": str(message)}, 500

