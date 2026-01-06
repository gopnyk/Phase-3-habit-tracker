from DB1 import DBHandler
from datetime import date, timedelta

class DemoData:
    def __init__(self):
        super().__init__()
        self.db = DBHandler("DB1.db")



    def insert_daily_habit_w_streak(self):
        reading_id = self.db.insert_habit_sql("Reading", "30 minutes before sleep, to wind down", "daily", None, 10)

        test_creation_date_1 = date.today() - timedelta(days=10)

        test_creation_date_1 = test_creation_date_1.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_1, "Reading",))

        # reading  - current streak = 3, best streak = 3,  5 completions, 6 days missed

        # 6 missed =  date.today() - timedelta(i)  , i = 10,7,6,5,4,3

        reading_completion_dates = []

        #
        for i in range(0, 3):
            reading_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))

        reading_completion_dates.append((date.today() - timedelta(days=8)).strftime("%Y-%m-%d"))
        reading_completion_dates.append((date.today() - timedelta(days=9)).strftime("%Y-%m-%d"))

        for i in reading_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (reading_id, i))

    def insert_weekly_habit_w_streak(self):
        running_id = self.db.insert_habit_sql("Running", "The classic 2 km route through the bridge and fields.", "weekly", None, 10)

        test_creation_date_2 = date.today() - timedelta(days=40)

        test_creation_date_2 = test_creation_date_2.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_2, "Running",))

        # ~~~~~~~~ Running -  5 completions, best streak =3 , current streak =3, missed = 3

        running_completion_dates = []

        for i in range(1, 15, 4):
            running_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))

        # one additional completion date
        running_completion_dates.append((date.today() - timedelta(days=38)).strftime("%Y-%m-%d"))

        for i in running_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (running_id, i))


    def insert_monthly_habit(self):
        cleaning_id = self.db.insert_habit_sql("Garage cleaning", "Bring out trash, wipe the windows, clean the shelves, leave the automobile space clean. Wash the towels and disinfect tools", "monthly", None, 10)

        test_creation_date_2 = date.today() - timedelta(days=180)

        test_creation_date_2 = test_creation_date_2.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_2, "Garage cleaning",))


        running_completion_dates = []


        for i in range(1, 180, 29):
            running_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))


        for i in running_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (cleaning_id, i))


    def insert_custom_habit(self):
        equipment_id = self.db.insert_habit_sql("Technical configuration", "Every two days, the technical video and audio equipment should be reconfigured, while construction is going on", "custom", 2, 30)

        test_creation_date_2 = date.today() - timedelta(days=45)

        test_creation_date_2 = test_creation_date_2.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_2, "Technical configuration",))


        technical_completion_dates = []


        for i in range(1, 45, 4):
            technical_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))


        for i in technical_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (equipment_id, i))


    def insert_custom_habit_2(self):
        vitamins_id =self.db.insert_habit_sql("Vitamins", "Every four days, consume a dose of omega-3, D3, K2 and Magnesium", "custom", 4, 30)

        test_creation_date_2 = date.today() - timedelta(days=60)

        test_creation_date_2 = test_creation_date_2.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_2, "Vitamins",))

        vitamin_completion_dates = []

        for i in range(10, 38, 4):
            vitamin_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))

        for i in vitamin_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (vitamins_id, i))


    def insert_monthly_habit_2(self):
        gathering_id = self.db.insert_habit_sql("Gathering with friends", "Organize a gathering with friends in a cafeteria. Bring some board games and snacks.", "monthly", None, 12)

        test_creation_date_2 = date.today() - timedelta(days=180)

        test_creation_date_2 = test_creation_date_2.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_2, "Gathering with friends",))

        gathering_completion_dates = []

        # 7 completions in a row

        for i in range(43, 148, 36):
            gathering_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))

        for i in gathering_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (gathering_id, i))


    def insert_daily_habit_2(self):
        meditation_id = self.db.insert_habit_sql("Meditation", "10 minute meditation before work", "daily", None, 30)

        test_creation_date_1 = date.today() - timedelta(days=25)

        test_creation_date_1 = test_creation_date_1.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_1, "Meditation",))


        meditation_completion_dates = []

        #
        for i in range(6, 45, 3):
            meditation_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))

        meditation_completion_dates.append((date.today() - timedelta(days=8)).strftime("%Y-%m-%d"))
        meditation_completion_dates.append((date.today() - timedelta(days=9)).strftime("%Y-%m-%d"))

        for i in meditation_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (meditation_id, i))


    def load_all(self):

        #insert the data
        self.insert_daily_habit_w_streak()
        self.insert_weekly_habit_w_streak()
        self.insert_monthly_habit()
        self.insert_custom_habit()
        self.insert_custom_habit_2()
        self.insert_monthly_habit_2()
        self.insert_daily_habit_2()
        # save the data
        self.db.conn.commit()

if __name__ == "__main__":

    #safeguard, for data input
    confirm = input("Are you sure you want to add demo data to the application? Type in: yes / no ")
    if confirm.lower() == "yes":
        DemoData().load_all()



