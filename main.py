import uvicorn
from fastapi import FastAPI, Response, Query
from pydantic import BaseModel, Field, field_validator
from enum import Enum




app = FastAPI()

class Operators(str, Enum):
    add = "+"
    sub = "-"
    mul = "*" or "x"
    div = "/"

class Temperature(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"
    kelvin = "kelvin"

class Calculator(BaseModel):
    first_number: float = Field(title="First number", description="Enter first number")
    second_number: float = Field(title="Second number", description="Enter second number")
    operation: Operators = Field(title="Operation", description="Enter operation", examples=["+", "-", "*", "/"])

    @field_validator("second_number")
    def validate_second_number(cls, v, values, **kwargs):
        """
        A validator function to check the second number based on the operation being performed.
        Parameters:
            cls: the class.
            v: the second number to be validated.
            values: a dictionary containing the values.
            **kwargs: additional keyword arguments.
        Returns:
            The validated second number.
        """
        second_number = v
        

        if second_number == 0 and values["operation"] == Operators.div:
            raise ZeroDivisionError("Cannot divide by zero")
        return second_number

# Calculator Route
@app.post("/calculate")
async def calculate(calculator: Calculator, response: Response):
    """
    Calculate the result based on the provided calculator object and operation. 
    
    Parameters:
    - calculator: an instance of Calculator class containing the first_number, second_number, and operation.
    - response: an instance of Response class to handle the response status code.

    Returns:
    - The result of the calculation based on the operator provided in the calculator object.
    """
    first_number = calculator.first_number
    second_number = calculator.second_number
    operator = calculator.operation

    if operator == "+":
        response.status_code = 200
        return {"answer": first_number + second_number}
    if operator == "-":
        response.status_code = 200
        return {"answer": first_number - second_number}
    if operator == "*" or operator == "x":
        response.status_code = 200
        return {"answer": first_number * second_number}
    if operator == "/":
        response.status_code = 200
        return {"answer": first_number / second_number}
        
    


# Temperature Route
@app.get('/convert/temperature')
async def convert_temperature(response: Response, temp: float = Query(title="Temperature", description="Enter temperature"), from_unit: Temperature = Query(title="From Unit", description="Enter from unit", examples=["celsius", "fahrenheit", "kelvin"]), to_unit: Temperature = Query(title="To Unit", description="Enter to unit", examples=["celsius", "fahrenheit", "kelvin"])):
    """
    Convert temperature from one unit to another.

    Parameters:
    - temp: temperature to be converted
    - from_unit: unit to convert from
    - to_unit: unit to convert to

    Returns:
    - converted temperature
    """
    if from_unit == Temperature.celsius and to_unit == Temperature.fahrenheit:
        response.status_code = 200
        return {"answer": (temp * 1.8) + 32}
    if from_unit == Temperature.celsius and to_unit == Temperature.kelvin:
        response.status_code = 200
        return {"answer": temp + 273.15}
    if from_unit == Temperature.fahrenheit and to_unit == Temperature.celsius:
        response.status_code = 200
        return {"answer": (temp - 32) * 5/9}
    if from_unit == Temperature.fahrenheit and to_unit == Temperature.kelvin:
        response.status_code = 200
        return {"answer": (temp + 459.67) * 5/9}
    if from_unit == Temperature.kelvin and to_unit == Temperature.celsius:
        response.status_code = 200
        return {"answer": temp - 273.15}
    if from_unit == Temperature.kelvin and to_unit == Temperature.fahrenheit:
        response.status_code = 200
        return {"answer": (temp * 9/5) - 459.67}
    response.status_code = 200
    return {"answer": temp}
    

# Factorial Calculator Route
@app.get('/factorial')
def calculate_factorial(response: Response, number: int = Query(title="Number", description="Enter number", examples=[5,6,7,8], gt=0, lt= 20)):
    """
    Calculate the factorial of a number.

    Parameters:
    - number: number to calculate the factorial of

    Returns:
    - factorial of the number
    """
    if number == 0:
        response.status_code = 200
        return {"answer": 1}
        
    while number > 0:
        answer = number * calculate_factorial(number - 1)
    response.status_code = 200
    return {"answer": answer}

@app.post("/interest")
async def calculate_interest(amount: float, rate: float, time: int, response: Response):
    """
    Calculate the interest on an amount.

    Parameters:
    - amount: principal amount
    - rate: interest rate
    - time: time period in years

    Returns:
    - interest on the principal amount
    """
    interest = (amount * rate * time) / 100
    response.status_code = 200
    return {"answer": interest}

@app.get('/palindrome')
async def is_palindrome(text: str = Query(title="Text", description="Enter text to check if it is a palindrome", examples=["racecar", "madam", "level"])):
    new_word = text[::-1]


    if new_word == text:
        return {"answer": True}
    else:
        return {"answer": False}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)