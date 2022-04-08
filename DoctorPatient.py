print("Individual Project")
print("Patient/Doctor Scheduler")
import datetime
import sqlite3

class DBbase:
    _conn = None
    _cursor = None

    def __init__(self, db_name):
        self._db_name = db_name

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_script):
        self._cursor.executescript(sql_script)

    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn

    def close_db(self):
        self._conn.close()

    def reset_database(self):
        raise NotImplementedError()


# Individual is the Base Class with basic functionalities to be implemented by child class
class Individual(DBbase):
    def __init__(self):
        super().__init__("DoctorAppointmentSchedulerDB.sqlite")

    def update(self, *params):
        raise NotImplementedError

    def add(self, *params):
        raise NotImplementedError

    def delete(self, *params):
        raise NotImplementedError

    def fetch(self, *params):
        raise NotImplementedError



# Patient class inheriting from Individual Class
class Patient(Individual):

    # updates name,age and gender in a patient table
    def update(self, id, age, name):
        try:
            super().connect()
            super().get_cursor.execute("""UPDATE Patient SET  age = ? , name =? 
            WHERE id= ?""", (age, name, id))
            super().get_connection.commit()
            super().close_db()
            print("Patient record has been updated successfully!")
        except Exception as e:
            print("Error occurred while updating the Patient record.", e)

    # adds patient record in patient table.
    def add(self, name, age):
        try:
            super().connect()
            super().get_cursor.execute("""INSERT or IGNORE INTO Patient(name, age) 
                                          VALUES (?,?)""", (name, age))
            super().get_connection.commit()
            super().close_db()
            print("Patient added successfully in the database!")
        except Exception as e:
            print("Error occurred in adding patient ", e)

    # deletes patient record from the patient table
    def delete(self, id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM Patient WHERE id = ?""", (id,))
            super().get_connection.commit()
            super().close_db()
            print("Patient record deleted successfully!")
        except Exception as e:
            print("Error occurred in deleting patient record")

    # fetch() retrieves patient details based on id or name.
    def fetch(self, id=None, name=None):
        try:
            super().connect()
            if id is not None:
                return super().get_cursor.execute("""SELECT * FROM Patient WHERE id = ? """, (id,)).fetchone()
            elif name is not None:
                return super().get_cursor.execute("""SELECT * FROM Patient WHERE name = ?""", (name,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Patient""").fetchall()
        except Exception as e:
            print("Error occurred", e)
        finally:
            super().close_db()

    # resets the patient table
    def reset_database(self):
        sql = """
                DROP TABLE IF EXISTS Patient;
                
                CREATE TABLE Patient(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    name VARCHAR(20),
                    age INTEGER CHECK (age > 0));
            """
        super().execute_script(sql)


# Doctor class inherits from Individual Class
class Doctor(Individual):

    # updates the record in doctor table
    def update(self, id, availability, name=None, specialization=None):
        try:
            super().connect()

            if name is not None and specialization is not None:
                super().get_cursor.execute("""UPDATE Doctor
                                            SET name = ?, specialization = ?, availability = ? 
                                            WHERE id = ?""", (name, specialization, availability, id))
            # updates the availability for the doctor
            else:
                super().get_cursor.execute("""UPDATE Doctor
                                            SET availability = ? 
                                            WHERE id = ?""", (availability, id))
            super().get_connection.commit()
            super().close_db()
            print("Doctor record updated successfully!")
        except Exception as e:
            print("Error occurred while updating Doctor table.", e)

    # add() adds the doctor record in Doctor table
    def add(self, name, specialization, availability):
        try:
            super().connect()
            super().get_cursor.execute("""insert or ignore into Doctor(name, specialization ,availability) 
                                        values (?,?,?)""",
                                       (name, specialization, availability))
            super().get_connection.commit()
            super().close_db()
            print("Doctor added successfully!")
        except Exception as e:
            print("Error occurred in adding doctor ", e)

    # delete() removes the doctor record from the Doctor table.
    def delete(self, id):
        try:
            super().connect()
            super().get_cursor.execute("""delete from Doctor WHERE id = ?""", (id,))
            super().get_connection.commit()
            super().close_db()
            print("Doctor record deleted successfully!")
        except Exception as e:
            print("Error occurred in deleting doctor record")

    # fetch() retrieves doctor details based on the id, name provided
    def fetch(self, id=None, name=None):
        try:
            super().connect()
            if id is not None:
                return super().get_cursor.execute(
                    """SELECT * FROM Doctor WHERE id = ? """, (id,)).fetchone()
            elif name is not None:
                return super().get_cursor.execute("""SELECT * FROM Doctor WHERE name = ?""", (name,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Doctor""").fetchall()
        except Exception as e:
            print("Error occurred while fetching Doctor info", e)
        finally:
            super().close_db()

    # reset_database() resets the Doctor table
    def reset_database(self):
        sql = """
                DROP TABLE IF EXISTS Doctor;
                CREATE TABLE Doctor(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name VARCHAR(20),
                specialization VARCHAR(50),
                availability VARCHAR(100))            
                """
        super().execute_script(sql)


# It will add the time with a gap of 30 minutes.
timing = '09:00'
time_availability = []
i = 0
while i <= 16:
    date_time_obj = datetime.datetime.strptime(timing, '%H:%M')
    time_availability.append(date_time_obj.strftime('%H:%M'))
    timing = date_time_obj + datetime.timedelta(minutes=30)
    timing = timing.strftime('%H:%M')
    i = i + 1

print(time_availability)


# Appointment class inherits from DBbase class which manages the Doctor appointment.
class Appointment(DBbase):

    def __init__(self):
        super().__init__("DoctorAppointmentSchedulerDB.sqlite")

    # update() assigns back the schedule to doctor
    def update(self, patient_id, new_slot=None):
        try:
            patient_slot = ap.fetch_scheduling_details(patient_id)        # fetch doctor's available appointments
            appointment_availability = doctor.fetch(1, None)
            a = list(appointment_availability[3].split(','))
            a.append(patient_slot[0])
            doctor.update(1, ','.join(a))                            # assigned back the slot to doctor

        except Exception as e:
            print("Error occurred in updating Appointment!")

    # add() adds an appointment in the Schedule table
    def add(self, doctor_id, patient_id, appointment_time, visit_reason):
        try:
            super().connect()
            super().get_cursor.execute("""INSERT INTO Appointment(doctor_id, patient_id, appointment_time, 
            visit_reason) VALUES (?,?,?,?)""",(doctor_id, patient_id, appointment_time, visit_reason))
            super().get_connection.commit()
            super().close_db()
            print("Doctor added successfully!")
        except Exception as e:
            print("Error occurred in adding doctor", e)

    # delete() removes the Appointment record from the table
    def delete(self, id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM Appointment WHERE patient_id = ?""", (id,))
            super().get_connection.commit()
            super().close_db()
            print("Appointment record deleted successfully!")
        except Exception as e:
            print("Error occurred in deleting appointment!")

    # This function fetches the appointment time for the given patient.
    def fetch_scheduling_details(self, patient_id):
        try:
            super().connect()
            if id is not None:
                return super().get_cursor.execute(
                    """SELECT appointment_time FROM Appointment WHERE patient_id = ? """, (patient_id,)).fetchone()
        except Exception as e:
            print("Error occurred while fetching appointment details!", e)
        finally:
            super().close_db()

    # fetch_all_appointments() gets the count of appointments scheduled for the Doctor.
    def fetch_all_appointments(self, id):
        try:
            super().connect()
            if id is not None:
                return super().get_cursor.execute(
                    """SELECT COUNT(*) FROM Appointment WHERE doctor_id = ? """, (id,)).fetchone()
        except Exception as e:
            print("Error occurred while fetching doctor info!", e)
        finally:
            super().close_db()

    # reset_database() resets the Schedule table
    def reset_database(self):
        sql = """
                DROP TABLE IF EXISTS Appointment;
                CREATE TABLE Appointment(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                patient_id  INTEGER,
                doctor_id INTEGER,
                appointment_time VARCHAR(10),
                visit_reason VARCHAR(20),
                CONSTRAINT appointment_fkey_patient FOREIGN KEY (patient_id) REFERENCES patient (id),
                CONSTRAINT appointment_fkey_doctor FOREIGN KEY (doctor_id) REFERENCES doctor (id))
                """
        super().execute_script(sql)


ap = Appointment()
ap.connect()


appointment_options = {
    "book": "Book an appointment",
    "check": "Check if time is available",
    "getby" : "Get appointment details by name",
    "cancel": "Cancel an appointment",
    "exit": "Exit"
}

# The below code will iterate till the user inputs exit.
user_selection = None
while user_selection != "exit":
    print("Appointment Booking Menu and Details")
    for option in appointment_options.items():
        print(option)

    user_selection = input("Select an option:")

    doctor = Doctor()
    patient = Patient()
    appointment = Appointment()
    if user_selection == "book":            # This functionality is to book an appointment.
        no_of_appoint = appointment.fetch_all_appointments(1)
        if int(no_of_appoint[0]) < 16:             # This is to check if number of appointments < 16.
            patient_name = input("Enter your name: ")
            patient_age = int(input("Enter your age: "))
            patient.add(patient_name, patient_age)         # For adding Patient name and age to Patient Table
            patient_reason = input("Please mention reason for your visit: ")
            appointment_avail = doctor.fetch(1)       # This fetches available slots from Doctor Table
            print("Available timings: ", appointment_avail[3])
            user_timing = input("Enter time for booking an appointment:").strip()
            time = appointment_avail[3].split(',')
            while True:       # This block of code is for booking the appointment
                if user_timing in time:
                    p = patient.fetch(None, patient_name)
                    appointment.add(1, p[0], user_timing, patient_reason)
                    time.remove(user_timing)
                    doctor.update(1, ','.join(time), None, None)
                    print("Congratulations.Your appointment is booked.")
                    break;
                else:
                    print("Please enter timing from the available slots.")
                    user_timing = input("Enter the time book the appointment: ")
        else:
            print("Sorry.Appointments are full today.")

    if user_selection == "check":            # This functionality is to display all the available slots for today.
        try:
            number_appoint = appointment.fetch_all_appointments(1)
            if int(number_appoint[0]) < 16:
                print("Yes, doctor is available today!")
                appointment_avail = doctor.fetch(1)                             # fetching available slots
                print("Available Timings: ", appointment_avail[3])
            else:
                print("Sorry! Appointments are full today!")
        except Exception as e:
            print("Error occurred while retrieving the appointment details.")

    # This functionality checks whether the patient has already booked appointment or not.
    if user_selection == "getby":
        user_1 = input("Enter your name:")
        record = patient.fetch(None, user_1)
        if record is not None:
            print(record)
        else:
            print("Sorry you have not booked any appointment: ")

    # This functionality provides the patient an option to cancel the appointment.
    if user_selection == "cancel":
        cancel_confirm = input("Are you sure you want to cancel the appointment?: ")
        if cancel_confirm == 'yes':
            user1 = input("Please enter your name: ")
            record = patient.fetch(None, user1)
            apt = Appointment()
            if record is not None:   #Assign back the patient slot to available slots for next booking.
                apt.update(record[0], None)
                apt.delete(record[0])
                patient.delete(record[0])          # delete the patient record in Appointment table.
            else:                                  # when patient detail not found, print below message.
                print("Sorry! You ave not booked any appointment!")
        else:
            print("Thankyou!!")
