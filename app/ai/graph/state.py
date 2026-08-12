from typing import TypedDict,Optional 


# We are defining a state for the graph for the overall workflow ; 

class WorkflowState(TypedDict): 
    # always  needed inputs : 
    user_id: str
    session_id: str
    user_message :str 

    # filled by  understand node 
    target_concept : Optional[str]
    intent : Optional[str]

    # filled by the load-learner-state node : 
    learner_state : Optional[str]

    #filled by tutor node : 
    tutor_response : Optional[str]

    # use later for adaptive routing : 
    next_action:Optional[str] 

    