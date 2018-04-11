# -*- coding: utf-8 -*-
"""
Вытаскивает все посты из указанных разделов.
API Reference: https://2ch.pm/abu/res/42375.html
"""
import logging
import pickle
import signal
import sys
from multiprocessing.pool import Pool
from typing import List

import requests

EXIT_SUCCESS = 0
EXIT_UNKNOWN = 256


# posts = []


# def save_to_pkl():
#     with open("./posts.pkl", "wb") as file:
#         pickle.dump(posts, file, pickle.HIGHEST_PROTOCOL, fix_imports=False)


# noinspection PyBroadException
def main():
    log.debug(f"args: {sys.argv}")
    pool = Pool()
    raw_results: List[List[str]] = pool.map(process_board, sys.argv[1:])  # skip first arg (script path)

    posts = []
    for result in raw_results:
        posts.extend(result)

    log.info("done, saving...")
    with open("./posts.pkl", "wb") as file:
        pickle.dump(posts, file, pickle.HIGHEST_PROTOCOL, fix_imports=False)
    log.info("bye!")
    return EXIT_SUCCESS


def process_board(board: str) -> List[str]:
    posts = []
    # noinspection PyBroadException
    try:
        log.info(f"now processing {board}")
        board_json = requests.get(f"https://2ch.hk/{board}/catalog.json").json()
        log.debug(f"board len is {len(board_json)}")
        for thread in board_json["threads"]:
            thread_result, is_continue = process_thread(thread, board)
            posts.extend(thread_result)
            if not is_continue:
                return posts
    except (SystemExit, KeyboardInterrupt):
        return posts
    except Exception:
        log.error(f"Parsing board {board} failed!", exc_info=True)
    return posts


def process_thread(thread: dict, board: str) -> (List[str], bool):
    posts = []
    # noinspection PyBroadException
    try:
        num = thread["num"]
        thread_json = requests.get(
            f"https://2ch.hk/makaba/mobile.fcgi?task=get_thread&board={board}&thread={num}&post=0").json()
        for post in thread_json:
            posts.append(post["comment"])
    except (SystemExit, KeyboardInterrupt):
        return posts, False
    except Exception:
        log.error(f"Parsing thread {num} failed!", exc_info=True)
    return posts, True


# noinspection PyUnusedLocal
def exit_handler(sig=None, frame=None):
    # log.info("saving and exiting...")
    # save_to_pkl()
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
