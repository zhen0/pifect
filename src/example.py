## example Flow code
## this will only work off the deploy-2.0 branch of Prefect

import prefect
from prefect import task, Flow



@task(name="Welcome", slug="welcome-task")
def welcome_logger():
    logger = prefect.context["logger"]
    with open("/ascii-welcome.txt", "r") as f:
        lines = "\n\n" + "".join(f.readlines()) + "\n\n"

    logger.info(lines)

f = Flow("Welcome Flow", tasks=[welcome_logger])

## if we don't provide our own storage, Prefect will default to storing
## your flow in ~/.prefect/flows, and only agents running on this machine
## will be able to submit this flow for execution.
## At this time, your environment will be automatically labeled with 
## the labels ["local", "welcome-flow"]
f.register("Jenny") 
# f.run()

## now, we can run an appropriately configured agent for this flow 
## immediately in-process; this agent will listen for scheduled work
## from Prefect Cloud:
# f.run_agent() # spawns a local agent 

## we can also run an agent via CLI in the same way as before:
## (local agents will always label themselves "local")
# prefect agent start local -t TOKEN -l welcome-flow

## if we exit the process in which we created this Flow, we can always
## restore the Flow object via the Flow.load interface;
## if we were to recreate the Flow, we must call flow.deploy() again
## to re-register the Flow with its new Task IDs
#from prefect import Flow

#flow = Flow.load("welcome-flow")
#flow.run_agent()
