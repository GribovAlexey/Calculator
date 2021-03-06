from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.calculations import calculate_expression, validate_expression
from src.history import history, Status

app = FastAPI()


class CalcRequest(BaseModel):
    expression: str


@app.post("/calc/")
async def calc(item: CalcRequest):
    errors = validate_expression(item.expression)
    if errors:
        history.save_history(item.expression, errors, Status.FAIL)
        msg = "".join(["Invalid data: ", *errors])
        raise HTTPException(status_code=422, detail=msg)
    result = calculate_expression(item.expression)
    history.save_history(item.expression, response=result,
                         status=Status.SUCCESS)
    return result


@app.get("/history/")
async def get_history(limit: Optional[int] = None,
                      status: Optional[str] = None):
    errors = history.validate_attributes(limit=limit, status=status)
    if errors:
        msg = "".join(["Invalid attributes: ", *errors])
        raise HTTPException(status_code=422, detail=msg)
    return history.get_history(limit=limit, status=status)
