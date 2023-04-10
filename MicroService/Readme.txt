Microservice Application Using Python Flask > https://github.com/eupendra/book_store_microservice

Services >
User
Book
Order
Frontend


***USER****
User API - end points
/api/user/all - GET
/api/user/create - POST
/api/user/login - POST
/api/user/logout - POST
/api/user/<username>/exists - GET
/api/user/ - GET logged in user

mkdir user
cd user
#create virtual env
python -m venv .venv
.venev\Scripts\activate 
pip install Flask
echo > app.py
echo > routes.py

https://realpython.com/flask-blueprint/#:~:text=Each%20Flask%20Blueprint%20is%20an,before%20you%20can%20run%20it.
Blueprint > Each Flask Blueprint is an object that works very similarly to a Flask application. They both can have resources, such as static files, templates, and views that are associated with routes. However, a Flask Blueprint is not actually an application. It needs to be registered in an application before you can run it.

echo > models.py
python.exe -m pip install --upgrade pip
pip install sqlalchemy flask-sqlalchemy


https://flask-login.readthedocs.io/en/latest/
Flask-Login > provides user session management for Flask.
pip install flask-login


https://flask-migrate.readthedocs.io/en/latest/
pip install Flask-Migrate
after adding the migrate = Migrate(app,models.db)
On terminal run below command:
flask db init
flask db migrate 
flask db upgrade (this will create user.db in database)

Postman > to post the data 

#Logging in

whenever need to run the application activate the venv
.venv\Scripts\activate
.venv\Scripts\deactivate.bat


Error faced: 
sqlite:///../database/user.db
methods

***Book****

Book API - enpoints
/api/book/all - GET
/api/book/create - POST
/api/book/<slug> - GET

venv created
code . (opens vscode)

To create Secret key on vs code
python
import secrets
secrets.token_urlsafe(10)

pip install flask flask-sqlalchemy flask-migrate

***Order****

Order API - Endpoints
/api/order/ - GET
/api/order/all - GET
/api/order/add-item - POST
/api/order/checkout - POST


venv created
code . (opens vscode)
pip install flask flask-sqlalchemy flask-migrate requests
python.exe -m pip install --upgrade pip

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user
			
			
			
****FRONTEND****
pip install flask flask-login flask-bootstrap flask-wtf wtform



user-svc-c
book-svc-c
order-svc-c


****Docker****
docker network create --driver bridge micro_network
cd /user
docker build --tag user-svc .
docker run -p 5003:5003 -d --name user-svc-c -net=micro_network user-svc

cd /book
docker build --tag book-svc .
docker run -p 5001:5001 -d --name book-svc-c --net=micro_network book-svc

cd /order
docker build --tag order-svc .
docker run -p 5002:5002 -d --name order-svc-c --net=micro_network order-svc

cd /frontend
docker build --tag frontend-svc .
docker run -p 5000:5000 -d --name frontend-svc-c --net=micro_network frontend-svc

****Docker-compose****
docker-compose.yaml in microservice
docker-compose -f docker-compose.yml build
docker images
docker ps -a
docker-compose -f docker-compose.yml up -d


***Git***
git add .
git status
git commit -m "Microservice"
git status
git push -u origin main

git merge --abort

***kind on local***
#installing chocolatey package manager
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
#install kind
choco install kind -y
kind create cluster
kubectl cluster-info --context kind-kind
kubectl version
kubectl get pods
kubectl create ns test
vi deployment.yaml
kubectl apply -f deployment.yaml -n test
kubectl get pods -n test
kubectl get svc -n test
kubectl port-forward service/frontend-svc-c 5000:5000 -n test