from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass
class Person:
    name: str
    email: str


@dataclass
class Student:
    name: str
    mother: Person
    father: Person
    first_note: Optional[Decimal] = None
    second_note: Optional[Decimal] = None


class INotifyParent(AbstractClass):  # Abstract
    def notify(self, student: Student):
        to = self._get_emails(student)
        if self._verify_if_student_is_approved(student):
            print(f'Sending email to: {to}. Message: {self._get_success_message(student)}')
        else:
            print(f'Sending email to: {to}. Message: {self._get_fail_message(student)}')

    def _get_emails(self, student: Student) -> list[str]:  # Hook
        return [student.mother.email]

    @abstractmethod
    def _verify_if_student_is_approved(self, student: Student) -> bool:  # operation
        pass

    @abstractmethod
    def _get_success_message(self, student: Student) -> str:  # operation
        pass

    @abstractmethod
    def _get_fail_message(self, student: Student) -> str:  # operation
        pass


class NotifyParentAfterFirstNote(INotifyParent):
    def _verify_if_student_is_approved(self, student: Student) -> bool:
        if not student.first_note:
            raise ValueError("This student doesn't first note")
        elif student.first_note >= Decimal('7'):
            return True
        else:
            return False

    def _get_success_message(self, student: Student) -> str:
        return f'Congratulations to {student.name} on the first note'

    def _get_fail_message(self, student: Student) -> str:
        passing_grade = Decimal("7.00") + (Decimal("7.00") - (student.first_note or 0))
        return f'{student.name} must get an {passing_grade} to pass the next test'


class NotifyParentAfterSecondNote(INotifyParent):
    def _get_emails(self, student: Student) -> list[str]:
        return [student.mother.email, student.father.email]

    def _verify_if_student_is_approved(self, student: Student) -> bool:
        if not student.first_note:
            raise ValueError("This student doesn't have first note")
        elif not student.second_note:
            raise ValueError("This student doesn't have second note")
        elif ((student.first_note + student.second_note) / 2) >= Decimal('7'):
            return True
        else:
            return False

    def _get_success_message(self, student: Student) -> str:
        return f'Congratulations to {student.name} for the approval'

    def _get_fail_message(self, student: Student) -> str:
        return f'{student.name} is failed with an average of {(((student.first_note or 0) + (student.second_note or 0)) / 2)}'


class NotifyParentService:  # Context
    def __init__(self, notify_parent_after_first_note: INotifyParent, notify_parent_after_second_note: INotifyParent):
        self.__notify_parent_after_first_note = notify_parent_after_first_note
        self.__notify_parent_after_second_note = notify_parent_after_second_note

    def run(
        self,
        student: Student,
    ):
        if student.first_note and student.second_note:
            self.__notify_parent_after_second_note.notify(student)
        elif student.first_note:
            self.__notify_parent_after_first_note.notify(student)
        else:
            raise ValueError(f'{student.name} did not take tests')


notify_parent = NotifyParentService(NotifyParentAfterFirstNote(), NotifyParentAfterSecondNote())

notify_parent.run(
    Student(
        name='student',
        mother=Person(
            name='mother',
            email='mother@email.com',
        ),
        father=Person(
            name='father',
            email='father@email.com',
        ),
        first_note=Decimal('8'),
        second_note=None,
    )
)

notify_parent.run(
    Student(
        name='student',
        mother=Person(
            name='mother',
            email='mother@email.com',
        ),
        father=Person(
            name='father',
            email='father@email.com',
        ),
        first_note=Decimal('6'),
        second_note=None,
    )
)


notify_parent.run(
    Student(
        name='student',
        mother=Person(
            name='mother',
            email='mother@email.com',
        ),
        father=Person(
            name='father',
            email='father@email.com',
        ),
        first_note=Decimal('7'),
        second_note=Decimal('8'),
    )
)

notify_parent.run(
    Student(
        name='student',
        mother=Person(
            name='mother',
            email='mother@email.com',
        ),
        father=Person(
            name='father',
            email='father@email.com',
        ),
        first_note=Decimal('5'),
        second_note=Decimal('6'),
    )
)
