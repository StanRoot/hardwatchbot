import logging
import sys


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[1;31m",
    }
    RESET = "\033[0m"

    def format(self, record):
        text = super().format(record)
        color = self.COLORS.get(record.levelno, "")
        return f"{color}{text}{self.RESET}"


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ColorFormatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        force=True,
    )