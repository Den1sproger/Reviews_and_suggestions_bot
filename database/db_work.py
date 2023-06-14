import pymysql

from .db_config import *



class Database:
    """The class responsible for working with the database of rewievs and suggestions"""

    def connect_to_db(self):
        # Connect to the database
        # Подключение к базе данных
        connection = pymysql.connect(
            host=host, user=user, port=3306,
            password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    
    def connect_to_users_db(self):
        connection = pymysql.connect(
            host=host, user=user, port=3306,
            password=password, database=db_users,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    

    def get_list_of_full_data(self, query: str, users: bool = False) -> list[str]:
        if not users:
            connection = self.connect_to_db()
        else:
            connection = self.connect_to_users_db()
            
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()

        return [item.get(list(item.keys())[-1]) for item in data]
    

    def action(self, query: str) -> None:
        connection = self.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                except pymysql.err.IntegrityError:
                    connection.rollback()
            connection.commit()


    def __del__(self) -> int:
        return 0
