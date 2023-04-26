from typing import Optional, Union

from patterns.Singleton.implementations.main.typings import IData


class DataBase:
    __instance: Union[None, 'DataBase'] = None
    __DEFAULT_DATABASE_NAME = 'public'
    __data: IData = {
        'users': [
            {
                'id': 1,
                'username': 'foo',
            },
            {
                'id': 2,
                'username': 'bar',
            },
        ]
    }

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, database_name: Optional[str] = None):
        self.__database_name = database_name or self.__DEFAULT_DATABASE_NAME

    @property
    def database_name(self):
        return self.__database_name

    def get_data(self) -> IData:
        return self.__data

    def create_user(self, username: str):
        self.__data['users'].append(
            {
                'id': len(self.__data['users']),
                'username': username,
            }
        )


first_database_connection = DataBase()

first_database_connection.create_user('John')
first_database_connection.create_user('Mary')
first_database_connection.create_user('Paul')


print(first_database_connection.database_name)
print(first_database_connection.get_data())

second_database_connection = DataBase('secondary_db')

second_database_connection.create_user('Jennifer')
second_database_connection.create_user('Agatha')
second_database_connection.create_user('Arnold')

print(second_database_connection.database_name)
print(second_database_connection.get_data())
print(first_database_connection.database_name)
print(first_database_connection.get_data())
