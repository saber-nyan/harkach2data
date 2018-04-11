# -*- coding: utf-8 -*-
"""
Вытаскивает все посты из указанных разделов.
API Reference: https://2ch.pm/abu/res/42375.html
"""
import html
import logging
import pickle
import re
import signal
import sys

EXIT_SUCCESS = 0
EXIT_UNKNOWN = 256

REGEX_REMOVE_HTML = re.compile(r"<.*?>")
REGEX_REMOVE_REPLY = re.compile(r">>\d+")
REGEX_REMOVE_LINK = re.compile(r"https?://(\S*)")

result = []


# noinspection PyBroadException
def main():
    log.debug(f"args: {sys.argv}")
    with open(sys.argv[1], "rb") as file:
        data = pickle.load(file, fix_imports=False)
    log.info(f"posts count: {len(data)}")
    log.info("started!")
    out_file = open("./output_data.txt", "wt", encoding="utf-8", errors="ignore")
    for orig_msg in data:
        if len(orig_msg) <= 15:
            continue
        msg = orig_msg.replace("<br>", "\n")  # Replace <br> by \n
        msg = html.unescape(msg)  # Unescape HTML (&lt; for example)
        msg = REGEX_REMOVE_HTML.sub('', msg)  # Remove remaining HTML
        msg = REGEX_REMOVE_REPLY.sub('', msg)  # Remove replies (>>2)
        msg = REGEX_REMOVE_LINK.sub('', msg)  # Remove links (https://google.com)

        if msg in ["Bump", "bump", "бамп", "бамп", "ролл", "roll", "Ролл", "SAGE", "сажа"] and len(msg) <= 35:
            continue

        out_file.write(msg)
        out_file.write("\n")

    log.info("done!")
    file.close()
    return EXIT_SUCCESS


# noinspection PyUnusedLocal
def exit_handler(sig, frame):
    sys.exit(EXIT_SUCCESS)


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
        status = main()
    except:
        log.fatal("Unknown exception.", exc_info=True)
        exit(EXIT_UNKNOWN)
    # noinspection PyUnboundLocalVariable
    exit(status)
