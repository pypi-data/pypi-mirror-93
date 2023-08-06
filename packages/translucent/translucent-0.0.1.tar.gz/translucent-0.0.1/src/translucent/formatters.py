import datetime as dt
from pythonjsonlogger.jsonlogger import JsonFormatter
from tzlocal import get_localzone
import pytz


class JSON(JsonFormatter):
    _FIXED_FIELDS = ["namespace", "name"]
    _DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, *args, **kwargs):
        for field in self._FIXED_FIELDS:
            if field not in kwargs:
                raise ValueError(f"Logging configuration requires field '{field}'")
            setattr(self, field, kwargs.pop(field))
            self._timezone = get_localzone()
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("time"):
            # this doesn't use record.created, so it is slightly off
            log_record["time"] = self._to_utc(record.created).strftime(
                self._DATETIME_FORMAT
            )
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        for field in self._FIXED_FIELDS:
            log_record[field] = getattr(self, field)

    def _to_utc(self, timestamp):
        t = dt.datetime.fromtimestamp(timestamp)
        return self._timezone.localize(t, is_dst=None).astimezone(pytz.utc)
