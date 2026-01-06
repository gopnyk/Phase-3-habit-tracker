import sqlite3
import datetime
from datetime import date, timedelta, datetime
class DBHandler:
    def __init__(self, db_path="DB1.db"):
        import sqlite3
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        self.create_tables_sql()

    def create_tables_sql(self):
        # create tables if they don't exist
        self.c.execute("""CREATE TABLE IF NOT EXISTS habits_table(
                          ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          Habit_name TEXT NOT NULL UNIQUE,
                          Description TEXT,
                          Habit_type TEXT NOT NULL CHECK(Habit_type IN ('daily','weekly','monthly','custom')),
                          Custom_days INTEGER CHECK(Custom_days>0) DEFAULT NULL,
                          Goal_set INTEGER CHECK(Goal_set>0) DEFAULT NULL,
                          Creation_date DATE DEFAULT (DATE('now') )
                        )""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS mark_table(
                          ID INTEGER NOT NULL,
                          Mark_date DATE DEFAULT (DATE('now')),
                          CONSTRAINT unique_pair UNIQUE (ID, Mark_date),
                          CONSTRAINT fk_habit FOREIGN KEY (ID) REFERENCES habits_table(ID)
                        )""")
        self.conn.commit()



    #Will be used in add_habit() for habit creation
    def insert_habit_sql(self, name, description, habit_type, custom_days, goal_set):
        self.c.execute("""INSERT INTO habits_table  (Habit_name, Description, Habit_type, Custom_days, Goal_set)
            VALUES (?, ?, ?, ?, ?)""", (name.strip(), description, habit_type, custom_days, goal_set))
        self.conn.commit()
        #Fetching the ID, so we can save the habit locally
        return self.c.lastrowid


    def get_last_completion_date_sql(self,db_id):
        self.c.execute("""SELECT MAX(mark_date) FROM mark_table WHERE ID=?""",(db_id,))
        row = self.c.fetchone()
        if row and row[0]:
            return datetime.strptime(row[0], "%Y-%m-%d").date()
        return None

    def total_completed_sql(self,db_id):
        self.c.execute("SELECT COUNT(*) FROM mark_table WHERE ID = ?", (db_id,))
        return self.c.fetchone()[0] or 0


    def reset_records_sql(self,db_id):
        self.c.execute("""DELETE FROM mark_table WHERE ID = ?""", (db_id,))
        self.conn.commit()


    def check_name_sql(self, new_name):
        self.c.execute("""SELECT habit_name FROM habits_table WHERE habit_name = ?""", (new_name,))
        result = self.c.fetchone()
        return True if result else False



        #checks if there is a completion for today. If there is none, the user can mark a habit as completed for that day.
    # The record will be saved in the mark_table
    def mark_habit_sql(self, db_id, mark_date):
        if isinstance(mark_date, date):
            mark_date = mark_date.strftime("%Y-%m-%d")
        self.c.execute("SELECT ID FROM mark_table WHERE ID = ? AND mark_date = ?",(db_id,mark_date))

        if not self.c.fetchone():
            self.c.execute("INSERT INTO mark_table (ID, Mark_date) VALUES (?, ?)",(db_id,mark_date))
            self.conn.commit()

            return True
        return False


    def fetch_all_habits_sql(self):
        self.c.execute("SELECT ID, Habit_name, Description, Habit_type, Custom_days, Goal_set, creation_date FROM habits_table")
        return self.c.fetchall()

    def fetch_completion_dates_sql(self, db_id):
        self.c.execute("SELECT Mark_date FROM mark_table WHERE ID = ? ORDER BY Mark_date ASC", (db_id,))
        rows = self.c.fetchall()
        return [datetime.strptime(r[0], "%Y-%m-%d").date() for r in rows]


    def fetch_today_completed_id_sql(self):
        self.c.execute("""SELECT ID FROM mark_table WHERE mark_date = DATE('now')""")
        return [row[0] for row in self.c.fetchall()]

    def reset_todays_completion_sql(self,db_id):
        self.c.execute("""DELETE FROM mark_table WHERE ID= ? AND mark_date = DATE('now')""", (db_id,))
        self.conn.commit()

    def reset_completion_sql(self,db_id,chosen_date):
        if isinstance(chosen_date, date):
            chosen_date = chosen_date.strftime("%Y-%m-%d")
        self.c.execute("""DELETE FROM mark_table WHERE ID = ? AND mark_date = ? """,(db_id, chosen_date))
        self.conn.commit()

    def fetch_all_habit_names_sql(self):
        self.c.execute(("""SELECT habit_name FROM habits_table ORDER BY habit_name"""))
        return [row[0] for row in self.c.fetchall()]

    def rename_habit_sql(self,db_id, new_name):
        self.c.execute("""UPDATE habits_table SET habit_name = ? WHERE ID = ? """,(new_name,db_id))
        self.conn.commit()

    def change_description_sql(self,db_id, new_description):
        self.c.execute("""UPDATE habits_table SET description = ? WHERE ID = ? """, (new_description, db_id))
        self.conn.commit()

    def delete_habit_sql(self,db_id):
        self.c.execute("""DELETE FROM mark_table WHERE ID =?""",(db_id,))
        self.c.execute("""DELETE FROM habits_table WHERE ID =?""",(db_id,))
        self.conn.commit()

    def fetch_creation_date_sql(self, db_id):
        self.c.execute("""SELECT creation_date FROM habits_table WHERE ID = ?""", (db_id,))
        row = self.c.fetchone()
        if row and row[0]:
            return datetime.strptime(row[0], "%Y-%m-%d").date()
        return None

    def close_application_sql(self):
        try:
            if self.conn:
                self.conn.commit()
                self.conn.close()
        except:
            pass


    def reset_creation_date_sql(self,db_id):
        self.c.execute("""UPDATE habits_table SET creation_date = (DATE('now') )WHERE ID = ?""",(db_id,))
        self.conn.commit()


