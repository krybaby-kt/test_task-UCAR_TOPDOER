import enum


class IncidentStatusEnum(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"
    canceled = "canceled"


class IncidentSourceEnum(enum.Enum):
    operator = "operator"
    monitoring = "monitoring"
    partner = "partner"
    system = "system"
    user = "user"
    api = "api"
    web = "web"
    mobile = "mobile"
    other = "other"