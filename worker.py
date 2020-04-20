from rq import Connection, Worker

with Connection():
    qs = ['default']

    w = Worker(qs)
    w.work()
