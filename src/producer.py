import json
import random
import redis
import logging


def export(count=10) -> None:
    test = [{"metadata": {"from": 1111111111, "to": 2222222222}, "amount": 10000},
            {"metadata": {"from": 3333333333, "to": 4444444444}, "amount": -3000},
            {"metadata": {"from": 3333333333, "to": 4444444444}, "amount": 3000},
            {"metadata": {"from": 2222222222, "to": 5555555555}, "amount": 5000}]
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        for i in range(4):
            logging.info(r.publish("transfer", json.dumps(test[i])))
            logging.info(f"Message {test[i]} sent to server")
        for i in range(count):
            temp = generate()
            logging.info(r.publish("transfer", json.dumps(temp)))
            logging.info(f"Message {temp} sent to server")
    except redis.exceptions.ConnectionError as ex:
        logging.exception("[redis.exceptions.ConnectionError]", exc_info=True)


def generate():
    start_range = 1000000000
    end_range = 9999999999
    start_amount = -100000
    end_amount = 100000
    temp = {
        "metadata": {
            "from": random.randint(start_range, end_range),
            "to": random.randint(start_range, end_range),
        },
        "amount": random.randint(start_amount, end_amount)
    }
    return temp


if __name__ == "__main__":
    # Logging into file
    # logging.basicConfig(level=logging.INFO, filename="log_product.log", filemode="w+",
    #                     format="%(asctime)s %(levelname)s %(message)s")
    # Logging into stdout
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    export()
