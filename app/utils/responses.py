

def successful_response_message(message):
    return {"message": message}, 200

def bad_request_response_message(message):
    return {"message": message}, 400

