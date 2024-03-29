Building Access Management System

The Building Access Management System is a software application that manages the access of individuals in a building. Its purpose is to provide an efficient and secure solution for monitoring and recording personnel access.

The main features of the system include:
- Access Logging: The system records each access of personnel in a database, keeping information such as the person's ID, access date and time, entry/exit direction, and the gate used.
- Work Hours Monitoring: The system automatically calculates the worked hours for each employee based on access records, allowing for efficient work schedule management and identification of any deviations.
- Notifications for Insufficient Work Hours: If an employee has worked less than the prescribed number of hours, the system sends notifications to the respective managers to inform them of this situation.


File Contents:
- main.py: The main file of the application, which starts the server and the user interface.
- database_manager.py: The module responsible for connecting to the database and executing CRUD operations.
- file_manager.py: The module responsible for processing input files and backing them up.
- mail_sender.py: The module responsible for sending email notifications to managers in case of insufficient work hours.
- server.py: The module that defines and manages the system's API interface.
- constants.py : The file containing constant values used throughout the application, including database connection information.
- README.txt: This file, which provides essential information about the project and usage instructions.
