# -*- coding: utf-8 -*-
import logging


def setup_console_logger():
    logging.root.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(levelname)-8s] %(message)s', datefmt='%H:%M:%S'
    )
    StreamHandler = logging.StreamHandler()
    StreamHandler.setFormatter(formatter)
    StreamHandler.setLevel(logging.DEBUG)
    logging.root.addHandler(StreamHandler)

def setup_file_logger():
    pass