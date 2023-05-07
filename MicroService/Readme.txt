Microservice Application Using Python Flask > https://github.com/eupendra/book_store_microservice

User service > 
User API - end points
/api/user/all - GET
/api/user/create - POST
/api/user/login - POST
/api/user/logout - POST
/api/user/<username>/exists - GET
/api/user/ - GET logged in user

Book service >
Book API - enpoints
/api/book/all - GET
/api/book/create - POST
/api/book/<slug> - GET

Order service >
Order API - Endpoints
/api/order/ - GET
/api/order/all - GET
/api/order/add-item - POST
/api/order/checkout - POST
			
Frontend service

***Deployment using Docker***
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
docker images
docker ps -a

***Deployment using Kubernetes***
#Tested on GKE
kubectl create ns book-store
kubectl apply -f deployment.yaml -n book-store
kubectl get pods -n book-store
kubectl get svc -n book-store

