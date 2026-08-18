from pydantic import BaseModel
from typing import Optional


#What must the user input contain? The is defined by the following input_structure pydantic class object

class imput_structure(BaseModel):
    query : str
    temp : float
    retries : int #not used in real applications. providing this attribute for illustrative purpose only
    timeout: int

#What must response contain? The is defined by the following out_structure pydantic class object

class out_structure(BaseModel):
    #Note: We will have to create an empty class instance as the LLM output has to be passed into the class
    # Pydantic will not allow an empty class object. So make te attributes optional as hown below.
    response: Optional[str] = None
    model: Optional[str]= None
    prompt_tokens: Optional[int]= None
    completion_tokens: Optional[int]= None
    total_tokens: Optional[int]= None
    time_taken: Optional[int]= None

