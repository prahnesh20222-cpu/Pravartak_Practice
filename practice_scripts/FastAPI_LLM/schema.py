from pydantic import BaseModel

'''
What must the user input contain? The is defined by the following input_structure pydantic class object
'''
class imput_structure(BaseModel):
    query : str
    temp : float
    retries : float #not used in real applications. providing this attribute for illustrative purpose only
    timeout: int

'''
What must response contain? The is defined by the following out_structure pydantic class object
'''

class out_structure(BaseModel):
    response: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    time_taken: int

