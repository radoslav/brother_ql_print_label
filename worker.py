from rq import Connection, Worker

# Preload libraries
# import

with Connection():
    qs = ['default']

    w = Worker(qs)
    w.work()
