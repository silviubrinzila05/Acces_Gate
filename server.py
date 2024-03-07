from flask import Flask, request
from database_manager import DatabaseManager
from datetime import datetime
from file_manager import FileManager
import threading

app = Flask(__name__)

db_manager = DatabaseManager()
db_manager.connect()

# Endpoint pentru înregistrare utilizator
@app.route('/utilizatori', methods=['POST'])
def signup():
    user_data = request.json
    query = "INSERT INTO persoane (Id, Nume, Prenume, Companie, IdManager, Email) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_data["Id"], user_data["Nume"], user_data["Prenume"], user_data["Companie"], user_data["IdManager"], user_data["Email"])
    db_manager.execute_query(query, values)
    return 'Utilizator înregistrat', 200

# Endpoint pentru înregistrarea accesului
@app.route('/acces', methods=['POST'])
def access():
    access_data = request.json
    data = datetime.strptime(access_data["data"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO acces (Id_Persoana, Data, Sens, Poarta) VALUES (%s, %s, %s, %s)"
    values = (access_data["idPersoana"], data, access_data["sens"], access_data["idPoarta"])
    db_manager.execute_query(query, values)
    return 'Acces înregistrat', 200

if __name__ == '__main__':
    # Fir de execuție pentru monitorizarea constantă a folderului de intrare
    file_manager = FileManager(
        input_path="C:/Users/Silviu/Desktop/proiect/intrari/", 
        backup_path="C:/Users/Silviu/Desktop/proiect/backup_intrari/",
        db_manager=db_manager
    )
    monitor_thread = threading.Thread(target=file_manager.monitor_input_folder)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Pornire server Flask
    app.run(host='0.0.0.0', debug=True)
