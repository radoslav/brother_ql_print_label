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