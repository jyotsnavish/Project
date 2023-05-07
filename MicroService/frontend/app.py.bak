from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from routes import blueprint

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = 'CamIFpYP3bvg7Aczzd'
app.config['WTF_CSRF_SECRET_KEY'] = 'c6VHMlrg8Gy_aAxzcz'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.register_blueprint(blueprint)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_message = 'Please login.'
login_manager.login_view = 'frontend.login'

bootstap = Bootstrap(app)

@login_manager.user_loader
def load_user(user_id):
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)