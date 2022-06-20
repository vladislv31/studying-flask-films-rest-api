"""HTTP responses."""


def successful_response_message(message, result=None):
    response = {"message": str(message)}

    if result:
        response["result"] = result

    return response, 200


def bad_request_response_message(message):
    return {"message": str(message)}, 400


def not_found_request_response_message(message):
    return {"message": str(message)}, 404
