from prefect import flow, get_run_logger, task


@flow(name="problem-demo")
def problem_workflow():
    number_of_items = 888
    items = list(range(0, number_of_items))

    logger = get_run_logger()
    logger.info(f"Starting flow for list of {len(items)} items")

    results1 = task1.map(items)
    results2 = task2.map(results1)
    results3 = task3.map(results2)

    return results3


@task
def task1(item: int) -> dict:
    logger = get_run_logger()
    logger.info(f"Starting task1 for item {item}")
    return {"item": item}


@task
def task2(d: dict) -> dict:
    logger = get_run_logger()
    logger.info(f"Starting task2 for dict {d}")
    return {"item": d["item"] + 1}


@task
def task3(d: dict) -> dict:
    logger = get_run_logger()
    logger.info(f"Starting task3 for dict {d}")
    return {"item": d["item"] + 1}


if __name__ == "__main__":
    problem_workflow()