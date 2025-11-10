import enum


class IncidentStatusEnum(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"
    canceled = "canceled"