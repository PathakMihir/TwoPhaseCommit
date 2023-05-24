import logging
from typing import Union
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import controller


logger = logging.getLogger(__name__)
app = FastAPI(debug=True)


class FoodItem(BaseModel):
    food_name: str


class BookingModel(BaseModel):
    packet_id: int
    order_id: int


@app.post("/foodService/reserveFood/")
def reserve_food(food_item: FoodItem):
    reserve_id = controller.reserve_food(food_name=food_item.food_name)
    if reserve_id == -1:
        return {"status": "FAILURE", "driver_id": reserve_id}

    return {"status": "SUCCESS", "driver_id": reserve_id}


@app.post("/foodService/bookFood/")
def book_food(bookingModel: BookingModel):
    response = controller.book_food(packet_id=bookingModel.packet_id, order_id=bookingModel.order_id)
    return {"status": response}


if __name__ == "__main__":
    # Run the FastAPI server using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
