from datetime import datetime


def get_now(fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    now = datetime.now().strftime(fmt)
    return datetime.strptime(now, fmt)


def get_now_string(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    now = datetime.now().strftime(fmt)
    return now
