# -*- coding: utf-8 -*-
"""
Вытаскивает все посты из указанных разделов.
API Reference: https://2ch.pm/abu/res/42375.html
"""
import logging
import pickle
import signal
import sys

import requests

EXIT_SUCCESS = 0
EXIT_UNKNOWN = 256

posts = []


def save_to_pkl():
    with open("./posts.pkl", "wb") as file:
        pickle.dump(posts, file, pickle.HIGHEST_PROTOCOL, fix_imports=False)


# noinspection PyBroadException
def main():
    log.debug(f"args: {sys.argv}")
    for board in sys.argv[1:]:  # skip first arg (script path)
        try:
            log.info(f"now processing {board}")
            board_json = requests.get(f"https://2ch.hk/{board}/catalog.json").json()
            log.debug(f"board len is {len(board_json)}")
            for thread in board_json["threads"]:
                try:
                    num = thread["num"]
                    # print(num)
                    thread_json = requests.get(
                        f"https://2ch.hk/makaba/mobile.fcgi?task=get_thread&board={board}&thread={num}&post=0").json()
                    for post in thread_json:
                        posts.append(post["comment"])
                    # time.sleep(0.1)
                except Exception as e:
                    if isinstance(e, SystemExit):
                        exit_handler()
                    log.error(f"Parsing thread {num} failed!", exc_info=True)
        except Exception as e:
            if isinstance(e, SystemExit):
                exit_handler()
            log.error(f"Parsing board {board} failed!", exc_info=True)

    log.info("done, saving...")
    save_to_pkl()
    log.info("bye!")
    return EXIT_SUCCESS


# noinspection PyUnusedLocal
def exit_handler(sig=None, frame=None):
    log.info("saving and exiting...")
    save_to_pkl()
    exit(EXIT_SUCCESS)


if __name__ == '__main__':
    l_logger = logging.getLogger()
    l_logger.setLevel("DEBUG")
    l_logger_sh = logging.StreamHandler()
    l_logger_sh.setFormatter(logging.Formatter(
        "%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: %(message)s"))
    l_logger_sh.setLevel("DEBUG")
    l_logger.addHandler(l_logger_sh)

    log = l_logger

    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)
    # noinspection PyBroadException
    try:
        exit(main())
    except Exception as exc:
        if not isinstance(exc, SystemExit):
            log.fatal("Unknown exception.", exc_info=True)
            exit(EXIT_UNKNOWN)
