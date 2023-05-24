from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'change-me'
host = '127.0.0.1'
port = 3306
database = 'store'


def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


def reserve_food(food_name):
    Session = sessionmaker(bind=get_connection())
    session = Session()
    try:
        session.begin()
        db = get_connection()

        query1 = text("""SELECT id ,food_name from FOOD 
        WHERE food_name=  :food""")
        food_row = session.execute(query1, {'food': food_name}).fetchone()

        query2 = text("""
        SELECT id ,is_reserved, order_id from PACKET 
        WHERE is_reserved=false and order_id = NULL and food_id= :_food_id
        LIMIT 1
        FOR UPDATE
        """)
        reserving_food = session.execute(query2, {'_food_id': food_row[0]}).fetchone()

        query3 = text("""
        UPDATE DELIVERY
        SET is_reserved =true WHERE order_id= :current_order_id
        """)

        session.execute(query3, {'current_order_id': order_id})

        session.commit()
        session.close()
        return reserving_food[0]

    except Exception as e:
        # Rollback the transaction in case of any error
        session.rollback()
        print("Error occurred. Transaction rolled back.")
        return -1


def book_food(packet_id, order_id):
    Session = sessionmaker(bind=get_connection())
    session = Session()
    try:
        session.begin()
        db = get_connection()
        query1 = text("""
        UPDATE PACKET
        SET is_reserved = True AND
        SET order_id = :order
        WHERE id = :packet;
        """)

        session.execute(query1, {'packet': packet_id, 'order': order_id})
        session.commit()
        session.close()
        return "SUCCESS"


    except IntegrityError as e:
        # Rollback the transaction in case of any error
        session.rollback()
        print("Error occurred. Transaction rolled back.")
        return "FAILURE"
