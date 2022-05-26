from flaskr import app


@app.route('/')
def index():
    return 'Initial'

