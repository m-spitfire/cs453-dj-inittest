from dataclasses import dataclass, field

import constraints as constraints_
import fieldtype


# Hmm...
@dataclass
class FieldNode:
    type: fieldtype.FieldNodeType
    name: str
    constraints: set[constraints_.FieldConstraints] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class ModelNode:
    name: str
    fields: set[FieldNode] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.name)


if __name__ == "__main__":
    # As post_model has a field with type FieldNodeType.MODEL,
    # our dependancy checker know that it must create that field first
    post_model = ModelNode(
        name="Post",
        fields=set((
            FieldNode(
                type=fieldtype.Varchar(255),
                name="title",
                constraints=set((constraints_.NotNull()))
            ),
            FieldNode(
                type=fieldtype.Model,
                name="author",
            )
        ))
    )
