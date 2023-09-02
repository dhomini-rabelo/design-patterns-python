from datetime import datetime


class DatabaseConnection:
    def run_sql(self, query: str):
        pass


class LogManager:
    def log(self, message: str):
        now = datetime.now()
        print(f'[{now.strftime("%H:%M")}]  {message}')


class SendEmail:
    def __init__(self, host_email: str, password: str):
        self.__HOST_EMAIL = host_email
        self.__PASSWORD = password

    def send(self, to: str, message: str):
        pass


class NotificationManager:
    def notify(self, username: str, message: str):
        pass


class CreateUserFacade:
    def __init__(self):
        self.__database_connection = DatabaseConnection()
        self.__log_manager = LogManager()
        self.__email_sender = SendEmail('me@email.com', '123456')
        self.__notification_manager = NotificationManager()

    def run(self, username: str):
        self.__database_connection.run_sql(f'INSERT INTO users (username) VALUES ({username})')
        self.__log_manager.log(f'CREATING USER: {username}')
        self.__email_sender.send('owner@email.com', f'{username} was created')
        self.__notification_manager.notify(username, message='Add your friends')


create_user = CreateUserFacade()
create_user.run('John Doe')
