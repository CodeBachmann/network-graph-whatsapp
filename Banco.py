import MySQLdb
class CRUD:
    # Connect to the database
    def __init__(self):
        self.connection = MySQLdb.connect(
        host='',
        user='',
        passwd='',
        db='',
        autocommit=True,
        ssl={ 'rejectUnauthorized':'true' }

        )
        self.cursor = self.connection.cursor()

    def fazer_requisicao(self, query):
        try:
            # Create a cursor to interact with the database         
            self.cursor.execute(f"""{query}""")
            myresult = self.cursor.fetchall()

            return myresult
        
        except MySQLdb.Error as e:
            print(query)
            print("MySQL Error:", e)


    def fechar_banco(self):
            self.cursor.close()
            self.connection.close()