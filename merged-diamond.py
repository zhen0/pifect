import sys
import prefect
from prefect.engine.signals import LOOP
from prefect.tasks.control_flow import ifelse, merge
import Cython

options = dict(enumerate(sys.argv))
flow_name = options.get(1, "etl")
project_name = options.get(2, "Jenny")

print("Flow:", flow_name)
print("Project:", project_name)


@prefect.task
def condition():
    return True


@prefect.task
def create_data(initial_value):
    return [initial_value, initial_value * 2, initial_value * 3]


@prefect.task
def path1(item):
    return item / 10


@prefect.task
def path2(item):
    return item / 7.2


@prefect.task
def mult_fact(item):
    loop_payload = prefect.context.get("task_loop_result", {"amt": 5, "item": item})
    if loop_payload["amt"] > 0:
        raise LOOP(
            message=f"Keep going",
            result=dict(
                item=loop_payload["item"] * loop_payload["amt"],
                amt=loop_payload["amt"] - 1,
            ),
        )

    return loop_payload["item"]


@prefect.task
def aggregate(data):
    result = sum(data)
    logger = prefect.context.get("logger")
    logger.info("FINAL RESULT: {}".format(result))
    return result


with prefect.Flow(flow_name) as flow:
    starting_value = prefect.Parameter(name="initial_value", default=10)
    input_set = create_data(starting_value)

    result1 = path1.map(input_set)
    result2 = path2.map(input_set)

    ifelse(condition(), result1, result2)

    middle_set = merge(result1, result2)

    end_set = mult_fact.map(middle_set)
    result = aggregate(end_set)

flow.register(project_name=project_name, version_group_id="hello")
