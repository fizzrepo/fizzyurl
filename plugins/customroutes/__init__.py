from flask import render_template

def run(app, db, config):
    @app.route('/hello')
    def routes_hiroute():
        return "It works!"
    
    @app.route('/hello/<name>')
    def routes_helloname(name):
        return "Hello " + name + "!"

    @app.route('/template')
    def routes_template():
        return render_template('template.html', name='World')
    