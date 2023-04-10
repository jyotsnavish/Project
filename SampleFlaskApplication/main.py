from flask import Flask, request, render_template
import socket
 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'My first Flask application'
    
@app.route('/echo')
# ‘/’ URL is bound with hello_world() function.
def echo():
    data = []
    hostname = socket.gethostname()
    for key, value in request.args.items():
        data.append({'key':key, 'value':value})
    return render_template('echo.html', data=data, hostname=hostname)
    
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host ='0.0.0.0', port = 5000, debug=True)