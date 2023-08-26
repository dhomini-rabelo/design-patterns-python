from abc import ABC as AbstractClass, abstractmethod
from time import sleep


class IDatabaseConnection(AbstractClass):  # Subject
    @abstractmethod
    def get_table_data(self, table_name: str) -> list[dict]:
        pass


class DatabaseConnection(IDatabaseConnection):  # Real Subject
    __data: dict[str, list[dict]] = {'users': [], 'accounts': []}

    def get_table_data(self, table_name: str):
        self.__connect()
        return self.__data[table_name]

    def __connect(self):
        sleep(1)


class DatabaseConnectionProxyCache(IDatabaseConnection):  # Proxy
    __cache: dict[str, list[dict]] = {}

    def __init__(self, database_connection: DatabaseConnection):
        self.__database_connection = database_connection

    def get_table_data(self, table_name: str):
        if table_name not in self.__cache.keys():
            response = self.__database_connection.get_table_data(table_name)
            self.__cache[table_name] = response
        return self.__cache[table_name]


database_connection = DatabaseConnection()

database_with_cache = DatabaseConnectionProxyCache(database_connection)

print('DATABASE')

print(database_connection.get_table_data('users'))
print(database_connection.get_table_data('users'))
print(database_connection.get_table_data('users'))

print('CACHE DATABASE')

print(database_with_cache.get_table_data('users'))
print(database_with_cache.get_table_data('users'))
print(database_with_cache.get_table_data('users'))
print(database_with_cache.get_table_data('users'))
print(database_with_cache.get_table_data('users'))
