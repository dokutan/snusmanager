# snusmanager

## Development server

```sh
cd backend
flask --app snusmanager.py run
# http://localhost:5000/apidocs/

cd frontend
ng serve
# http://localhost:4200/
```

## Deployment with gunicorn
```sh
cd frontend
ng build
cp -r dist ../backend
cd ../backend
gunicorn snusmanager:app --bind "[::]:8000"
```

## Build a docker image
```sh
cd frontend
ng build
cd ..
podman build . -t snusmanager
podman run -it -p 8000:8000 -v ./db.sqlite:/app/db.sqlite localhost/snusmanager:latest
```
