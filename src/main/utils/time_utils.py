import dateutil.parser as date_parser

from typing import Optional
from datetime import datetime


def get_now(fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    now = datetime.now().strftime(fmt)
    return datetime.strptime(now, fmt)


def get_now_string(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    now = datetime.now().strftime(fmt)
    return now


def parse_date_2_datetime_object(
        text: str, *, fmt: str = "%Y-%m-%d %H:%M:%S", raise_exception: bool = True
) -> Optional[datetime]:
    try:
        parsed = date_parser.parse(text)
        return datetime.strptime(parsed.strftime(fmt), fmt)
    except Exception as e:
        if raise_exception:
            raise e
        return
