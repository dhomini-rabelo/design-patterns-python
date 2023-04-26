from typing import Union

from patterns.Singleton.implementations.main.typings import IData


class DataBase:
    __instance: Union[None, 'DataBase'] = None
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

print(first_database_connection.get_data())

second_database_connection = DataBase()

second_database_connection.create_user('Jennifer')
second_database_connection.create_user('Agatha')
second_database_connection.create_user('Arnold')

print(second_database_connection.get_data())


print(first_database_connection.get_data())
