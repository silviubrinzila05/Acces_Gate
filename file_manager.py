import os
import csv
import shutil
from datetime import datetime
import time
from database_manager import DatabaseManager

class FileManager:
    """
    Proceseaza fisierele txt si csv
    """
    def __init__(self, input_path, backup_path, db_manager):
        self.input_path = input_path
        self.backup_path = backup_path
        self.db_manager = db_manager

    def process_files(self):
        for filename in os.listdir(self.input_path):
            if filename.endswith(".txt") or filename.endswith(".csv"):
                file_path = os.path.join(self.input_path, filename)
                try:
                    if filename.endswith(".txt"):
                        self.process_text_file(file_path)
                    elif filename.endswith(".csv"):
                        self.process_csv_file(file_path)
                    self.backup_file(file_path)
                except Exception as e:
                    print(f"A apărut o eroare la procesarea fișierului {filename}: {str(e)}")

    def process_text_file(self, file_path):
        # Extrage numarul portii din numele fisierului
        file_name = os.path.basename(file_path)
        poarta_num = ''.join(filter(str.isdigit, file_name))

        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                data[-1] = data[-1].rstrip(';')
                datetime_obj = datetime.strptime(data[1], "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                query = "INSERT INTO acces (Id_Persoana, Data, Sens, Poarta) VALUES (%s, %s, %s, %s)"
                values = (data[0], formatted_date, data[2], poarta_num)
                self.db_manager.execute_query(query, values)

    def process_csv_file(self, file_path):
        # Extrage numarul portii din numele fisierului
        file_name = os.path.basename(file_path)
        poarta_num = ''.join(filter(str.isdigit, file_name))

        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                datetime_obj = datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                query = "INSERT INTO acces (Id_Persoana, Data, Sens, Poarta) VALUES (%s, %s, %s, %s)"
                values = (row[0], formatted_date, row[2], poarta_num)
                self.db_manager.execute_query(query, values)

    def backup_file(self, file_path):
        filename = os.path.basename(file_path)
        today = datetime.now().strftime("%Y-%m-%d")
        new_filename = f"{os.path.splitext(filename)[0]}_{today}{os.path.splitext(filename)[1]}"
        shutil.move(file_path, os.path.join(self.backup_path, new_filename))
        print(f"Fișierul {filename} a fost mutat în folderul de backup cu numele {new_filename}.")

    def monitor_input_folder(self):
        while True:
            for filename in os.listdir(self.input_path):
                if filename.endswith(".txt") or filename.endswith(".csv"):
                    file_path = os.path.join(self.input_path, filename)
                    if os.path.isfile(file_path):
                        print(f"A fost detectat un nou fișier: {filename}")
                        self.process_files()
            time.sleep(1)

