from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'change-me'
host = '127.0.0.1'
port = 3306
database = 'store'


# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


def reserve_driver():
    Session = sessionmaker(bind=get_connection())
    session = Session()
    try:
        session.begin()
        db = get_connection()
        query1 = text("""
        SELECT id ,is_reserved, order_id from DELIVERY 
        WHERE is_reserved is false and order_id is NULL 
        LIMIT 1
        FOR UPDATE
        """)
        delivery_order = session.execute(query1).fetchone()


        query2 = text("""
        UPDATE DELIVERY
        SET is_reserved=true WHERE order_id= :delivery_id
        """)

        session.execute(query2,{"delivery_id":delivery_order[0]})
        session.commit()
        session.close()

        return delivery_order[0]

    except IntegrityError as e:
        # Rollback the transaction in case of any error
        session.rollback()
        print("Error occurred. Transaction rolled back.")
        return -1


def book_driver(driver_id, order_id):
    Session = sessionmaker(bind=get_connection())
    session = Session()
    try:
        session.begin()
        db = get_connection()
        query1 = text("""
        UPDATE DELIVERY
        SET is_reserved = True AND
        SET order_id = :order
        WHERE id = :driver;
        """)

        session.execute(query1, {'driver': driver_id, 'order': order_id})
        session.commit()
        session.close()

        return "SUCCESS"

    except IntegrityError as e:
        # Rollback the transaction in case of any error
        session.rollback()
        print("Error occurred. Transaction rolled back.")
        return "FAILURE"

if __name__ =="__main__":
    reserve_driver()