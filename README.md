# resources

https://github.com/pklaus/brother_ql

https://github.com/pklaus/brother_ql_web

https://github.com/splitbrain/bql-label-printer

## flask qr

  https://testdriven.io/blog/asynchronous-tasks-with-flask-and-redis-queue/
  https://github.com/mjhea0/flask-redis-queue

## run app
  export FLASK_APP=app.py
  pipenv run flask run --host=0.0.0.0
  
## run worker
  pipenv run python worker.py # or # pipenv run rq worker

## run app ass service
put services in 
/etc/systemd/system/

redis must by install
  sudo apt install redis
  
### run webserver flask
/etc/systemd/system/spooler-web.service
```
[Unit]
Description=Spooler Web

Requires=network.target
After=network.target

Requires=redis.service
After=redis.service

[Service]
User=radoslav
Group=radoslav
WorkingDirectory=/home/radoslav/git/brother_ql_print_label
Type=simple
ExecStart=/home/radoslav/.local/bin/pipenv run flask run --host=0.0.0.0

[Install]
WantedBy=default.target
```
### run worker

/etc/systemd/system/spooler-web-worker.service

```
[Unit]
Description=Spooler Web Worker

Requires=network.target
After=network.target

Requires=redis.service
After=redis.service

Requires=spooler-web.service
After=spooler-web.service

[Service]
User=radoslav
Group=radoslav
WorkingDirectory=/home/radoslav/git/brother_ql_print_label
Type=simple
ExecStart=/home/radoslav/.local/bin/pipenv run python worker.py

[Install]
WantedBy=default.target
```

# default ops

```
brother_ql print -l 62 ~/git/brother_ql_print_label/img/test.png
deprecation warning: brother_ql.devicedependent is deprecated and will be removed in a future release
{'label': '62', 'images': (<_io.BufferedReader name='/home/radoslav/git/brother_ql_print_label/img/test.png'>,), 'rotate': 'auto', 'threshold': 70.0, 'dither': False, 'compress': False, 'red': False, 'dpi_600': False, 'lq': False, 'cut': True}
```

```
docker run --name brother-redis -p 6379:6379 -d redis
docker stop brother-redis && docker rm brother-redis
```