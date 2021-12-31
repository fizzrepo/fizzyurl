def run(app):
    @app.route('/hi')
    def example():
        return "It works!"
