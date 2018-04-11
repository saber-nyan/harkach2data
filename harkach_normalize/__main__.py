# -*- coding: utf-8 -*-
"""
Удаляет из постов весь HTML, заменяет HTML-escape на оригинальные символы,
исключает некоторы посты, не несущие смысловой нагрузки.
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
DOUBTFUL_WORDS = ["Bump", "bump", "бамп", "Бамп",
                  "Ролл", "ролл" "roll", "Roll", ]  # Raise characters limit
BAD_WORDS = ["САЖА", "SAGE",
             "Главная Настройка Mobile Контакты NSFW ", "[ b / vg / po / news ]"]  # Skip possible wipe

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
        msg = msg.replace("(OP)", "")  # Remove "(OP)"

        if any(x in msg for x in DOUBTFUL_WORDS) and len(msg) <= 35:  # https://stackoverflow.com/a/3389611
            continue

        if any(x in msg for x in BAD_WORDS):
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
