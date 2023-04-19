from dataclasses import dataclass


class FieldConstraints:
    def __hash__(self) -> int:
        return id(self)
        # hash(self)


@dataclass
class NotNull(FieldConstraints):
    def __hash__(self) -> int:
        return super().__hash__()


@dataclass
class Unique(FieldConstraints):
    def __hash__(self) -> int:
        return super().__hash__()
