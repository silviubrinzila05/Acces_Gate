from database_manager import DatabaseManager
from file_manager import FileManager
from server import app
from mail_sender import calculate_work_hours
import threading
import time

def main():
    db_manager = DatabaseManager()
    db_manager.connect()

    file_manager = FileManager(
        input_path="C:/Users/Silviu/Desktop/proiect/intrari/", 
        backup_path="C:/Users/Silviu/Desktop/proiect/backup_intrari/",
        db_manager=db_manager
    )

    monitor_thread = threading.Thread(target=file_manager.monitor_input_folder)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Pornire server Flask într-un fir de executie separat
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'debug': True, "use_reloader" :False})
    flask_thread.daemon = True
    flask_thread.start()

    while True:
        calculate_work_hours()
        # Astept 24 de ore intre fiecare verificare a orelor lucrate
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    main()
