import mysql.connector

class DatabaseManager:
    """
    Clasa pentru conectare si interogare baza de date
    """
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "05081994"
        self.database = "cladire"
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Conexiune reușită la baza de date.")
        except mysql.connector.Error as error:
            print("A apărut o eroare la conectarea la baza de date:", error)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Deconectat de la baza de date.")

    def execute_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Query executat cu succes.")
        except mysql.connector.Error as error:
            print("A apărut o eroare la executarea query-ului:", error)

