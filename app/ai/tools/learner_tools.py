# we will have two tools here , one to get the learners profile and another one to read mastery for one concept . 

from __future__ import annotations
from typing import Any 
from langchain_core.tools import tool

from app.ai.tools.serialization import to_jsonable
from app.ai.tools.tool_context import get_safe_reads

@tool 
def get_learner_state(user_id: str) -> Any :
    """
    Fetch the learner's profile and known knowledge state.

    User this tool when additional information about the learner is needed to personalize
    the response . 
    """

    #read the custom learnerstate object from the service . 
    result = get_safe_reads().get_learner_state(user_id)

    #convert it into a dictionary that the LLM can understand . 
    return to_jsonable(result)



@tool 
def get_mastery(user_id : str, concept_id : str) -> Any :
    """
    Fetch mastery and confidence for one learner and concept. 
    An unknow result means there is not enough evidence yet . 
    """

    #ask the learner service for this user's concept mastery .
    result = get_safe_reads().get_mastery(
        
        user_id= user_id, 
        concept_id= concept_id)

    #convert it into a dictionary that the LLM can understand . 
    return to_jsonable(result)

