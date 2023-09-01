from structural_patterns.Composite.template.component.index import Serializer
from structural_patterns.Composite.template.component.typings import ISerializerSettings
from structural_patterns.Composite.template.validators.char import CharFieldValidator
from typing import Optional


class PersonSerializer(Serializer):
    name: str
    age: Optional[int]

    class Meta(ISerializerSettings):
        validator = {'name': CharFieldValidator(max_length=10)}


class SchoolSerializer(Serializer):
    student: PersonSerializer  # parent
    director: PersonSerializer  # parent
    name: str


s = SchoolSerializer()

print(
    s.validate(
        {
            'student': {
                'name': 'John Doe',
                'age': '14',
            },
            'director': {'name': 'Mary'},
            'name': 'MIT',
        }
    )
)
