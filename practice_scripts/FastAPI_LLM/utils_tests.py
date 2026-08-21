## Contains unit test functions for utils.py#
import sys, os
#sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import pytest
from utils import calculate_interest,fetch_stock_date,call_openai

#unless this is instaled, the decorator is not useful
#pip install pytest-asyncio
#note: we are not importing py-test-asyncio explicitly
#if our function is async, we'd have to build async test functions
@pytest.mark.asyncio
async def test_calculate_simple_interest_basic1():
    result = await calculate_interest(5000,6.5,2.5)
    assert result == {"interest": 812.5, "total_amount" : 5812.5}

@pytest.mark.asyncio
async def test_calculate_simple_interest_basic2():
    result = await calculate_interest(5000,0,2.5)
    assert result == {"interest": 0, "total_amount" : 5000}

#How do we test external components? We cannot exactly define output
# We have to mock them
# For e.g., the LLM response may be different everytime we call it
# mocking a reponse is done using the library respx

import respx, httpx

@pytest.mark.asyncio
@respx.mock
async def test_fetch_stock_data():
    # Use url__startswith to catch requests with dynamic query parameters
    respx.get("https://www.alphavantage.co/query").mock(
        return_value=httpx.Response(
            200, 
            json={'Time Series (5min)': {"09:03:01": {"1. open": "150.00"}}}
        )
    )
    
    result = await fetch_stock_date("AAPL")

    assert result is not None
    assert 'Time Series (5min)' in result
# WE are testing the output of the function assuming the api call is succeful
#how do I test API calls?

from unittest.mock import MagicMock
from unittest.mock import patch, AsyncMock
@pytest.mark.asyncio
async def test_call_openai():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "hello"
    mock_response.model = 'gpt-4'
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens=12
    mock_response.usage.total_tokens=22

    with patch('utils.client.chat.completions.create',
               new=AsyncMock(return_value=mock_response)):
        

        result = await call_openai("hi",0.2,3,60)
        assert result['response']=="hello"
        assert result['model'] == 'gpt-4'
        assert result['prompt_tokens'] == 10
        assert result['completion_tokens'] == 12
        assert result['total_tokens']==22
    
