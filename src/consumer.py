import json
import redis
import logging
import sys


def redis_listen(r, argc) -> None:
    queue = r.pubsub()
    queue.subscribe("transfer")
    logging.info("Subscribe to transfer created")
    data = []
    for message in queue.listen():
        if type(message['data']) is not int:
            data.append(swap(json.loads(message['data']), argc))
    logging.info("Listening ended")


def swap(info, argc) -> dict:
    if info['amount'] >= 0 and info['metadata']['to'] in argc:
        info['metadata']['from'], info['metadata']['to'] = info['metadata']['to'], info['metadata']['from']
    logging.info(f"Message: {info}")
    return info


def try_to_connect(argc):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_listen(r, argc)
    except redis.exceptions.ConnectionError as ex:
        logging.exception("[redis.exceptions.ConnectionError]", exc_info=True)


def parce_argv() -> list:
    r_value = []
    params = len(sys.argv)
    if params > 2 and sys.argv[1] == '-e':
        r_value = list(map(int, sys.argv[2].rstrip().split(',')))
    else:
        if params == 1:
            logging.critical("This .py file doesn't works without -e [list of account numbers] parameters")
        elif params == 2 and sys.argv[1] != '-e':
            logging.critical("You gave srange flag")
        elif params == 2 and sys.argv[1] == '-e':
            logging.critical("You on right way, next time give number of account with seperator=','")
    logging.info(f"Argv parsed is {r_value}")
    return r_value


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try_to_connect(parce_argv())
