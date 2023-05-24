import logging
from typing import Union
import uvicorn
import requests
from fastapi import FastAPI


app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

order_id = 1


@app.post("/orderService/order")
def order():
    global order_id;
    food_booking_url = 'http://localhost:8080'

    delivery_agent_booking_url = 'http://localhost:8081'
    payload = {}
    order_id = order_id
    order_id += 1

    # reserve food
    logger.info("Reserving Food.....")
    reserve_food_payload = {"food_name": "maggie"}
    logger.info(reserve_food_payload)
    reserve_food_response = requests.post(food_booking_url+"/foodService/reserveFood/",json=reserve_food_payload)
    logger.info(reserve_food_response.json())
    if reserve_food_response.json()["status"]!="SUCCESS":
        return "FAILED"
    # reserve delivery agent
    reserve_delivery_payload = {}
    logger.info("Reserving Delivery Agent.....")
    reserve_delivery_response = requests.post(delivery_agent_booking_url+"deliveryService/reserveDriver/", json=reserve_delivery_payload)
    if reserve_delivery_payload["status"]!="SUCCESS":
        return "FAILED"
    # book food
    logger.info("Booking Food....")
    book_food_payload = {"packet_id": reserve_food_response["packet_id"], "order_id":order_id}
    book_food_response = requests.post(food_booking_url+"/foodService/bookFood", json=book_food_payload)
    if book_food_response["status"]!="SUCCESS":
        return "FAILED"
    # book agent
    logger.info("Booking Delivery Agent....")
    book_delivery_payload = {"driver_id": reserve_delivery_response["driver_id"],order_id:order_id}
    book_deliver_response = requests.post(delivery_agent_booking_url+"/deliveryService/bookDriver", json=book_delivery_payload)
    if book_deliver_response["status"]!="SUCCESS":
        return "FAILED"

    return {"status":"SUCCESS","message":"Order is place with order_id:{}".format(order_id)}





if __name__ == "__main__":
    # Run the FastAPI server using Uvicorn
    #order()
    uvicorn.run(app, host="0.0.0.0", port=8000)
