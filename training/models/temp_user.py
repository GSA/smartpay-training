from dataclasses import dataclass, asdict


@dataclass
class TempUser:
    email: str
    first_name: str
    last_name: str
    agency: str  # maybe an id?

    def to_dict(self):
        return asdict(self)
