from datetime import datetime

KEY_TIMESTAMP = 'TIMESTAMP'
PADS_TIME_FORMAT = '%Y.%m.%d.%H.%M.%S'


def read_timestamp(line: str) -> datetime:
    """reads a pads timestamp and returns a datetime object
        TIMESTAMP year.month.day.hour.minute.second
    """
    entries = line.split()
    if entries[0] != KEY_TIMESTAMP:
        raise ValueError('given line is not a valid Timestamp line')
    return datetime.strptime(entries[1], PADS_TIME_FORMAT)