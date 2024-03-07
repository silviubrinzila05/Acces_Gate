from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime, timedelta
import csv
import mysql.connector
import os

class MailSender:
    """
    Calculeaza orele lucrate si trimite mail
    """
    __password = "daor mwbw vzps ezxr"
    __email_sender = 'brinzilasilviu58@gmail.com'

    def send_email(self, email_destinatie, subiect, body):
        em = EmailMessage()
        em['From'] = self.__email_sender
        em['To'] = email_destinatie
        em['Subject'] = subiect
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.__email_sender, self.__password)
            smtp.sendmail(self.__email_sender, email_destinatie, em.as_string())



BACKUP_DIR = "C:/Users/Silviu/Desktop/proiect"

def write_to_csv(results):
    backup_path = os.path.join(BACKUP_DIR, "backup")
    os.makedirs(backup_path, exist_ok=True)
    with open(os.path.join(backup_path, f"{datetime.now().strftime('%Y-%m-%d')}_chiulangii.csv"), "w", newline='') as csvfile:
        fieldnames = ['Nume', 'OreLucrate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            nume = result[0]
            prenume = result[1]
            ore_lucrate = result[4]

            # Verifica daca orele lucrate sunt mai putin de 8 ore si sunt disponibile
            if ore_lucrate is not None and ore_lucrate.total_seconds() / 3600 < 8:
                # Extrage orele, minutele si secundele
                ore = ore_lucrate.seconds // 3600
                minute = (ore_lucrate.seconds % 3600) // 60
                secunde = ore_lucrate.seconds % 60

                # Formateaza timpul
                timp_formatat = f"{ore} ore, {minute} minute, {secunde} secunde"

                writer.writerow({'Nume': nume + ' ' + prenume, 'OreLucrate': timp_formatat})

def write_to_txt(results):
    backup_path = os.path.join(BACKUP_DIR, "backup")
    os.makedirs(backup_path, exist_ok=True)
    with open(os.path.join(backup_path, f"{datetime.now().strftime('%Y-%m-%d')}_chiulangii.txt"), "w") as txtfile:
        for result in results:
            nume = result[0]
            prenume = result[1]
            ore_lucrate = result[4]

            # Verifica daca orele lucrate sunt mai putin de 8 ore si sunt disponibile
            if ore_lucrate is not None and ore_lucrate.total_seconds() / 3600 < 8:
                # Extrage orele, minutele si secundele
                ore = ore_lucrate.seconds // 3600
                minute = (ore_lucrate.seconds % 3600) // 60
                secunde = ore_lucrate.seconds % 60

                # Formateaza timpul
                timp_formatat = f"{ore} ore, {minute} minute, {secunde} secunde"

                txtfile.write(nume + ' ' + prenume + ',' + timp_formatat + '\n')




def calculate_work_hours():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="05081994",
        database="cladire"
    )

    cursor = db_connection.cursor()

    query = """
    SELECT 
        p.Nume,
        p.Prenume,
        p.Email,
        p.IdManager,
        TIMEDIFF(MAX(CASE WHEN a.Sens = 'out' THEN a.Data END), MAX(CASE WHEN a.Sens = 'in' THEN a.Data END)) AS OreLucrate
    FROM 
        persoane p
    JOIN 
        acces a ON p.Id = a.Id_Persoana
    WHERE 
        DATE(a.Data) = CURDATE()
    GROUP BY 
        p.Id
    """

    cursor.execute(query)
    results = cursor.fetchall()

    write_to_csv(results)
    write_to_txt(results)

    mail_sender = MailSender()

    for result in results:
        nume = result[0]
        prenume = result[1]
        email_angajat = result[2]
        id_manager = result[3]
        ore_lucrate = result[4]

        # Verifica dacă ore_lucrate este None
        if ore_lucrate is None:
            timp_formatat = "Nu sunt date disponibile"
        else:
            # Extrage orele, minutele și secundele
            ore = ore_lucrate.seconds // 3600
            minute = (ore_lucrate.seconds % 3600) // 60
            secunde = ore_lucrate.seconds % 60

            # Formatează timpul
            timp_formatat = f"{ore} ore, {minute} minute, {secunde} secunde"

        # Trimitere email catre managerul asociat angajatului
        if ore_lucrate is not None and ore_lucrate.total_seconds() / 3600 < 8:
            query_manager = """
            SELECT Email
            FROM persoane
            WHERE Id = %s
            """
            cursor.execute(query_manager, (id_manager,))
            manager_row = cursor.fetchone()
            if manager_row is not None:
                email_manager = manager_row[0]
                mail_sender.send_email(email_manager, "Atentie! Ore lucrate insuficiente", f"Angajatul {nume} {prenume} a lucrat doar {timp_formatat} astăzi.")
            else:
                print("Nu s-a găsit nicio adresă de email pentru manager.")


            mail_sender.send_email(email_manager, "Atentie! Ore lucrate insuficiente", f"Angajatul {nume} {prenume} a lucrat doar {timp_formatat} astăzi.")


if __name__ == "__main__":
    current_time = datetime.now()
    if current_time.hour >= 13:
        calculate_work_hours()
        print("Am trimis cu succes emailurile.")
