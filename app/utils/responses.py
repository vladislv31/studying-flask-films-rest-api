

def successful_response_message(message):
    return {"message": message}, 200


def bad_request_response_message(message):
    return {"message": message}, 400


def unauthorized_request_response_message(message="Access denied."):
    return {"message": message}, 401


def not_found_request_response_message(message):
    return {"message": message}, 404

