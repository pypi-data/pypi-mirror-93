import datetime as dt
from pythonjsonlogger.jsonlogger import JsonFormatter


class JSON(JsonFormatter):
    _FIXED_FIELDS = ["namespace", "name"]
    _DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, *args, **kwargs):
        for field in self._FIXED_FIELDS:
            if field not in kwargs:
                raise ValueError(f"Logging configuration requires field '{field}'")
            setattr(self, field, kwargs.pop(field))
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("time"):
            log_record["time"] = dt.datetime.fromtimestamp(record.created).strftime(
                self._DATETIME_FORMAT
            )
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        for field in self._FIXED_FIELDS:
            log_record[field] = getattr(self, field)
