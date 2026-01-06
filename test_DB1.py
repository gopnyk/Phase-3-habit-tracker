
from DB1 import DBHandler
from datetime import date, timedelta
import pytest



"""
This file tests the functionality of the DB1 database

Each that returns a value or manipulates the tables  will be tested

first all the functions that manipulate the database will be tested


"""

# no need to check the create tables function, because there is nothing to assert

class TestDatabase:

    # setting up a local environment to test the database functions
    def setup_method(self):
        self.db = DBHandler(":memory:")




    #~~~~~~~~~~~~~~~~~~~~~~~ Testing insert_habits_sql() function


        #Testing whether the function returns the habits id, once it is added to the database
    def test_insert_habit(self):

        # test whether the habit id is returned after the function is launched
        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily",None, 5)
        assert habit_id == 1

        #test whether the stored habit can be retrieved

        retrieved_habit =  self.db.fetch_all_habits_sql()
        assert len(retrieved_habit) == 1

        db_id, name, desc, habit_type, custom_days, goal, creation_date = retrieved_habit[0]

        assert name == "Reading"
        assert desc == "5mins"
        assert habit_type == "daily"
        assert custom_days is None
        assert goal == 5



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Testing mark_habit_sql()


    def test_mark_habit(self):


        today = date.today()

        habit_id =self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        #inserting a completion for today
        check = self.db.mark_habit_sql( habit_id,today)

        assert check is True

        #retrieving the completion

        completion_date = self.db.fetch_completion_dates_sql(habit_id)

        assert completion_date == [today]

    def test_mark_habit_duplicates(self):
        today = date.today()

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        # inserting a completion for today
        assert self.db.mark_habit_sql( habit_id,today) == True
        assert self.db.mark_habit_sql(habit_id, today) == False

        completion_dates = self.db.fetch_completion_dates_sql(habit_id)
        assert completion_dates == [today]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ delete_habit_sql()

    def test_delete_habit(self):
        #Creating two habits to ensure the correct one was deleted
        #The habits will have one completion date for today

        today = date.today()

        habit_id_1 = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)
        self.db.mark_habit_sql(habit_id_1, today)

        habit_id_2 =self.db.insert_habit_sql("Running", "5m", "weekly", None, 10)
        self.db.mark_habit_sql(habit_id_2, today)


        # deleting "Running" habit and its completions

        self.db.delete_habit_sql(habit_id_2)

        #The only habit should remain "Reading"
        habits = self.db.fetch_all_habits_sql()
        assert len(habits) == 1

        # testing whether the name matches

        db_id, name , description, habit_type, custom_days, goal_set, creation_date =habits[0]

        assert db_id == habit_id_1
        assert name == "Reading"


        # The completions for "Reading" should be today in a list and for "Running" an empty list:

        assert self.db.fetch_completion_dates_sql(habit_id_1) == [today]
        assert  self.db.fetch_completion_dates_sql(habit_id_2) == []




    #~~~~~~~~~~~~~~~~ reset_completion_sql()


    def test_reset_completion(self):
        # create a habit and mark today for complete

        today = date.today()

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)
        self.db.mark_habit_sql(habit_id, today)


        # resetting completion
        self.db.reset_completion_sql(habit_id,today)

        # asserting, the completion date list should be empty:

        assert self.db.fetch_completion_dates_sql(habit_id) == []




    # ~~~~~~~~~~~~~~~~ reset_todays_completion_sql()

    def test_reset_todays_completion(self):
        # create a habit and mark today for complete

        today = date.today()

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)
        self.db.mark_habit_sql(habit_id, today)

        # resetting completion for today
        self.db.reset_todays_completion_sql(habit_id)

        # asserting, the completion date list should be empty:

        assert self.db.fetch_completion_dates_sql(habit_id) == []



    # ~~~~~~~~~~~~~~~~ reset_records_sql()

    def test_reset_records_sql(self):
        # create a habit and mark today for complete

        today = date.today()
        three_days_ago = today - timedelta(days=3)

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        #shift back the creation date by 3 days
        self.db.conn.execute("""UPDATE habits_table SET creation_date = ? WHERE habit_name = ?""",
            (three_days_ago, "Reading"))

        self.db.conn.commit()


        #Mark the shifted creation day and today
        self.db.mark_habit_sql(habit_id, today)
        self.db.mark_habit_sql(habit_id, three_days_ago)

        # Deleting the records

        self.db.reset_records_sql(habit_id)

        assert self.db.fetch_completion_dates_sql(habit_id) == []




    #~~~~~~~~~~~~~~~~ reset_completion_sql()

    def test_reset_completion_sql(self):
        today = date.today()
        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        self.db.mark_habit_sql(habit_id, today)

        self.db.reset_completion_sql(habit_id,today)

        assert self.db.fetch_completion_dates_sql(habit_id) == []


    #~~~~~~~~~~~~~ rename_habit_sql()
    def test_rename_habit(self):

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        self.db.rename_habit_sql(habit_id,"Workout")

        habits = self.db.fetch_all_habits_sql()

        assert len(habits) == 1

        db_id, name, desc, habit_type, custom_days, goal, creation_date = habits[0]

        assert name == "Workout"
        assert desc == "5mins"
        assert habit_type == "daily"
        assert custom_days is None
        assert goal == 5


    #~~~~~~~~~~~~ change_description_sql()

    def test_change_description(self):

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        self.db.change_description_sql(habit_id,"10 pages")


        habits = self.db.fetch_all_habits_sql()
        assert len(habits) == 1

        db_id, name, desc, habit_type, custom_days, goal, creation_date = habits[0]

        assert name == "Reading"
        assert desc == "10 pages"
        assert habit_type == "daily"
        assert custom_days is None
        assert goal == 5


    #~~~~~~~~~~~ reset_creation_date_sql()

    def test_reset_creation_date(self):
        # create a habit and mark today for complete

        today = date.today()
        three_days_ago = today - timedelta(days=3)

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        # shift back the creation date by 3 days
        self.db.conn.execute("""UPDATE habits_table SET creation_date = ? WHERE habit_name = ?""",
                             (three_days_ago, "Reading"))

        self.db.conn.commit()


        # resetting the creation date to today
        self.db.reset_creation_date_sql(habit_id)

        habits = self.db.fetch_all_habits_sql()
        assert len(habits) == 1

        db_id, name, desc, habit_type, custom_days, goal, creation_date = habits[0]

        assert name == "Reading"
        assert desc == "5mins"
        assert habit_type == "daily"
        assert custom_days is None
        assert goal == 5
        assert date.fromisoformat(creation_date) == today



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ READ FUNCTIONS

    #~~~~~~~~~ fetch_all_habits_sql()

    def test_fetch_all_habits(self):

        #creating the habits
        self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)
        self.db.insert_habit_sql("Running", "2km", "weekly", None, 3)


        #fetching the habits
        habits = self.db.fetch_all_habits_sql()
        assert len(habits) == 2

        #testing and asserting the retrieved habits

        db_id, name, desc, habit_type, custom_days, goal, creation_date = habits[0]
        db_id2, name2, desc2, habit_type2, custom_days2, goal2, creation_date2 = habits[1]

        assert name == "Reading"
        assert desc == "5mins"
        assert habit_type == "daily"
        assert custom_days is None
        assert goal == 5

        assert name2 == "Running"
        assert desc2 == "2km"
        assert habit_type2 == "weekly"
        assert custom_days2 is None
        assert goal2 == 3



    #~~~~~~~~~~~~~~~ fetch_all_habit_names_sql()

    def test_fetch_all_habit_names(self):

        #inserting two unique habits
        self.db.insert_habit_sql("Zumba", "5mins", "daily", None, 5)
        self.db.insert_habit_sql("Aikido", "20min", "weekly", None, 3)


        #fetching all the names  - they come alphabetically sorted
        names = self.db.fetch_all_habit_names_sql()

        assert names[0] == "Aikido"
        assert names[1]  == "Zumba"



    #~~~~~~~~~~~~~ fetch_completion_dates_sql()

    def test_fetch_completion_dates(self):
        # create a habit and mark today for complete

        today = date.today()
        three_days_ago = today - timedelta(days=3)

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        # shift back the creation date by 3 days
        self.db.conn.execute("""UPDATE habits_table SET creation_date = ? WHERE habit_name = ?""",
                             (three_days_ago, "Reading"))

        self.db.conn.commit()

        # Mark the shifted creation day and today
        self.db.mark_habit_sql(habit_id, today)
        self.db.mark_habit_sql(habit_id, three_days_ago)

        # fetching the completion dates -
        dates = self.db.fetch_completion_dates_sql(habit_id)

        assert dates == [three_days_ago,today]



    #~~~~~~~~~~~~~~ get_last_completion_date_sql()
    def test_get_last_completion_date(self):
        # create a habit and mark today for complete

        today = date.today()
        three_days_ago = today - timedelta(days=3)

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        # shift back the creation date by 3 days
        self.db.conn.execute("""UPDATE habits_table SET creation_date = ? WHERE habit_name = ?""",
                             (three_days_ago, "Reading"))

        self.db.conn.commit()

        # Mark the shifted creation day and today
        self.db.mark_habit_sql(habit_id, today)
        self.db.mark_habit_sql(habit_id, three_days_ago)

        # fetching the last completion
        test_date = self.db.get_last_completion_date_sql(habit_id)

        assert test_date == today



    #~~~~~~~~~~ total_completed_sql()

    def test_total_completed(self):
        # create a habit and mark today for complete

        today = date.today()
        three_days_ago = today - timedelta(days=3)

        habit_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        # shift back the creation date by 3 days
        self.db.conn.execute("""UPDATE habits_table SET creation_date = ? WHERE habit_name = ?""",
                             (three_days_ago, "Reading"))

        self.db.conn.commit()

        # Mark the shifted creation day and today
        self.db.mark_habit_sql(habit_id, today)
        self.db.mark_habit_sql(habit_id, three_days_ago)

        # retrieving the total number or completions
        total_completed = self.db.total_completed_sql(habit_id)

        assert total_completed == 2

    #~~~~~~~~~~~~~~~~ check_name_sql()


    def test_check_name(self):
        #insert a habit
        self.db.insert_habit_sql("Reading", "5mins", "daily", None, 5)

        #checking whether the names are taken

        check_good = self.db.check_name_sql("Reading")
        check_bad = self.db.check_name_sql("Not reading")

        assert check_good == True
        assert  check_bad == False











































































