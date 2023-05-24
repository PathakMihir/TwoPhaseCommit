import logging
from typing import Union

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import controller

logger = logging.getLogger(__name__)
app = FastAPI(debug=True)


class BookingModel(BaseModel):
    order_id: int
    driver_id: int


@app.post("/deliveryService/reserveDriver")
def reserve():
    driver_id = controller.reserve_driver()
    if driver_id == -1:
        return {"status": "FAILURE", "driver_id": driver_id}

    return {"status": "SUCCESS", "driver_id": driver_id}


@app.post("/deliveryService/bookDriver")
def book(booking: BookingModel):
    response = controller.book_driver(booking.driver_id, booking.order_id)
    return {"status": response}


if __name__ == "__main__":
    # Run the FastAPI server using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
