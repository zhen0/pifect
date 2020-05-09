# from prefect import Flow, task
# from prefect.serialization.flow import FlowSchema

# @task
# def print_something():
#     print('ok')

# f = Flow("ex", tasks=[print_something])
# f.run() # prints ok

# s = FlowSchema()
# f2 = s.load(f.serialize())

# f2.tasks # has print_something task

# f2.run() # doesn't print

import os

bob = os.environ.get("DOCKER_HOST", "<unix://var/run/docker.sock>")
print(bob)