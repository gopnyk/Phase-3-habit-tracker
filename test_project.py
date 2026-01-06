from DB1 import DBHandler
from Habits import HabitControl
from datetime import date, timedelta
import pytest


class TestCounter:



    def setup_method(self):
        self.db = DBHandler(":memory:")
        self.hc = HabitControl(self.db)
        # 4 Test records
        # using sql functions, for a better test




    #~~~~~~~~~~~~~~~~~~~~~ helper insert functions, for testing

    def insert_daily_habit_w_streak(self):
        reading_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 10)

        test_creation_date_1 = date.today() - timedelta(days=10)

        test_creation_date_1 = test_creation_date_1.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_1, "Reading",))

        # reading  - current streak = 3, best streak = 3,  5 completions, 6 days missed

        # 6 missed =  date.today() - timedelta(i)  , i = 10,7,6,5,4,3

        reading_completion_dates = []

        #
        for i in range(0,3):
            reading_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))

        reading_completion_dates.append((date.today() - timedelta(days=8)).strftime("%Y-%m-%d"))
        reading_completion_dates.append((date.today() - timedelta(days=9)).strftime("%Y-%m-%d"))

        for i in reading_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (reading_id, i))


    def insert_daily_habit_no_streak(self):
        reading_id = self.db.insert_habit_sql("Reading", "5mins", "daily", None, 10)

        test_creation_date_1 = date.today() - timedelta(days=10)

        test_creation_date_1 = test_creation_date_1.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_1, "Reading",))

        # reading  - current streak = 0, best streak = 3,  5 completions, 5 days missed
        reading_completion_dates = []

        #
        for i in range(1,4):
            reading_completion_dates.append((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"))

        reading_completion_dates.append((date.today() - timedelta(days=8)).strftime("%Y-%m-%d"))
        reading_completion_dates.append((date.today() - timedelta(days=9)).strftime("%Y-%m-%d"))

        for i in reading_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (reading_id, i))




    def insert_weekly_habit_w_streak(self):
        running_id = self.db.insert_habit_sql("Running", "2km", "weekly", None, 10)

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

    def insert_weekly_habit_no_completions(self):


        running_id = self.db.insert_habit_sql("Running", "2km", "weekly", None, 10)

        # expected to get 4 missed completions from the creation day
        test_creation_date_2 = date.today() - timedelta(days=35)

        test_creation_date_2 = test_creation_date_2.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_2, "Running",))




    def insert_weekly_habit_completed(self):
        running_id = self.db.insert_habit_sql("Running", "2km", "weekly", None, 2)

        test_creation_date_2 = date.today() - timedelta(days=14)

        test_creation_date_2 = test_creation_date_2.strftime("%Y-%m-%d")

        self.db.c.execute("UPDATE habits_table SET Creation_date=? WHERE habit_name=?",
                          (test_creation_date_2, "Running",))

        # ~~~~~~~~ Running -  2 completions, best streak =1 , current streak =0, missed

        running_completion_dates = []

        # one additional completion date
        running_completion_dates.append((date.today() - timedelta(days=14)).strftime("%Y-%m-%d"))
        running_completion_dates.append((date.today() - timedelta(days=8)).strftime("%Y-%m-%d"))

        for i in running_completion_dates:
            self.db.c.execute("INSERT INTO mark_table (ID , mark_date) VALUES (?,?) ", (running_id, i))


    # ~~~~~~~~~~~~~~~~~~~~~ helper insert functions, for testing


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ANALYTICS MODULE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


    #~~~~~~~~~~~~~~~~~~~~ streak()

    # The most crucial analysis function -  streak(). Performing streaks for 2 different types - weekly and daily
    # because, the categories work in the same way, the results are dependent on set_interval variable. So if both work fine
    # the other classes will also work.


    #1) Daily test  - current streak and best streak (if broken), correct missed and completion dates
    #2) Weekly test - current streak and best streak (if broken), correct missed and completion dates
    #3) No completion test - weekly habit, tested with no completions at all. Focus on correct missed dates.




    def test_streak_and_dates_daily(self):
        #insert the  running id
        self.insert_daily_habit_w_streak()

        #load the habits - initiate streak function
        self.hc.load_habits()

        habit = self.hc.habits[0]

        assert habit.current_streak == 3
        assert habit.best_streak == 3
        assert habit.completions_missed == 6

        # today - timedelta(i)
        missed_intervals = [10,7,6,5,4,3]


        # 2 in a row, then broken, by 4 day missed interval
        # current streak should be 3 and best streak should be 3 as well.
        completed_intervals = [9,8,2,1,0]

        
        # testing correct missed dates
        test_missed_dates = set()
        test_completed_dates = []

        for i in missed_intervals:
            test_missed_dates.add(date.today() - timedelta(i))

        assert habit.missed_dates == test_missed_dates


        # testing correct completion dates

        for i in completed_intervals:
            test_completed_dates.append(date.today() - timedelta(i))

        assert habit.completion_dates == test_completed_dates

    def test_broken_streak_and_dates_daily(self):

        # insert the running id
        self.insert_daily_habit_no_streak()

        # load the habits - initiate streak function
        self.hc.load_habits()

        habit = self.hc.habits[0]

        #testing whether the current streak is broken
        assert habit.current_streak == 0
        assert habit.best_streak == 3
        assert habit.completions_missed == 6

        # today - timedelta(i)
        missed_intervals = [10, 7, 6, 5, 4, 0]

        # 2 in a row, then broken, by 4 day missed interval
        # current streak should be 3 and best streak should be 3 as well.
        completed_intervals = [9, 8, 3, 2, 1]

        # testing correct missed dates
        test_missed_dates = set()
        test_completed_dates = []

        for i in missed_intervals:
            test_missed_dates.add(date.today() - timedelta(i))

        assert habit.missed_dates == test_missed_dates

        # testing correct completion dates

        for i in completed_intervals:
            test_completed_dates.append(date.today() - timedelta(i))

        assert habit.completion_dates == test_completed_dates

    def test_no_completions_weekly(self):
        # insert the running habit
        self.insert_weekly_habit_no_completions()

        # load the habits - initiate streak function
        self.hc.load_habits()

        #fetching the habit
        habit = self.hc.habits[0]

        # testing whether we get 5 missed completions and no streaks
        assert habit.current_streak == 0
        assert habit.best_streak == 0
        assert habit.completions_missed == 5

        #testing the missed completion dates:
        #starts from creation date and every +7 days we expect a missed date

        today = date.today()
        creation_date = today - timedelta(days=35)

        test_missed_dates = set()

        #start counting days from creation date, including it itself
        first_missed_date= creation_date +timedelta(6)

        test_missed_dates.add(first_missed_date)

        # adding increments of 7 to the first missed date. It is done 4 times.
        for i in range(7,34,7):
            new_missed = first_missed_date + timedelta(i)
            test_missed_dates.add(new_missed)

        #asserting the completion dates and missed dates
        assert habit.completion_dates == []
        assert habit.missed_dates == test_missed_dates



    #~~~~~~~~~~~~~~~~~~~~ streak()



    #~~~~~~~~~~~~~~~~~~~~ calculate_dates()

    # To test this function, the test will be broken down into 3 cases:

    #1) No completions
    #2) Some completions
    #3) Completed habit


    # 1) NO COMPLETIONS:

    def test_calculate_dates_no_completions(self):
        #inserting the empty weekly habit

        self.insert_weekly_habit_no_completions()

        # load the habits - initiate streak function
        self.hc.load_habits()

        # fetching the habit
        habit = self.hc.habits[0]

        creation_date = habit.creation_date


        # calculating the approximate completion and next deadline
        # subtracting 1 from the interval set, because the creation date must be included
        approximate_completion = creation_date + timedelta( (7 * habit.reps_left) -1)

        next_deadline = creation_date + timedelta(7-1)

        assert approximate_completion == habit.approximate_completion

        assert next_deadline == habit.next_deadline

    # 2) SOME COMPLETIONS
    # goal_set = 10 , set_interval = 7

    def test_calculate_dates_w_completions(self):
        self.insert_weekly_habit_w_streak()

        # load the habits - initiate streak function
        self.hc.load_habits()

        # fetching the habit
        habit = self.hc.habits[0]

        #reference dates for calculations

        last_completion_date = habit.completion_dates[-1]



        #calculating the deadline and approximate completion

        approximate_completion = last_completion_date + timedelta((7 * habit.reps_left))

        next_deadline = last_completion_date + timedelta(7)

        # asserting the values

        assert approximate_completion == habit.approximate_completion
        assert  next_deadline == habit.next_deadline


    # 3) COMPLETED

    def test_calculate_dates_completed_habit(self):

        self.insert_weekly_habit_completed()

        # load the habits - initiate streak function
        self.hc.load_habits()

        # fetching the habit
        habit = self.hc.habits[0]

        #asserting the values

        assert habit.approximate_completion == "Goal achieved!"
        assert habit.next_deadline == " - "

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculate_dates()



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculate_consistency_ratio()

    # Important to test these cases

    # 1) Division by 0
    # 2) Correct ratio



    #1) Division by 0
    def test_consistency_ratio_div_zero(self):

        #adding an empty habit
        self.hc.add_habit("Test_name", "Test_desc", "daily", 10)


        # habit has no completions or missed dates, therefore there will be 0 in the denominator
        # asserting that consistency ration is 0

        # load the habits - initiate streak and consistency ration function
        self.hc.load_habits()

        habit = self.hc.habits[0]

        assert habit.consistency_ratio == 0


    #2) Correct ratio
    def test_consistency_ratio(self):

        #inserting the previously used "Reading" habit
        # reading  -   5 completions, 6 days missed, goal count = 10

        self.insert_daily_habit_w_streak()

        # load the habits
        self.hc.load_habits()

        #select the habit
        habit = self.hc.habits[0]

        #calculating the consistency manually
        true_consistency_ratio =  (5/(5+6)) *100

        #calculating the consistency with local data
        variable_consistency_ratio = (habit.completed_reps / (habit.completed_reps+habit.completions_missed)) *100


        #asserting the values
        assert true_consistency_ratio == habit.consistency_ratio
        assert  variable_consistency_ratio == habit.consistency_ratio



    #~~~~~~~~~~~~~~~~ Calculate_consistency_ratio()



    #~~~~~~~~~~~~~~~~ Calculate_completion_ratio()



    def test_completion_ratio(self):

        #inserting the habit with completions
        # reading -  5 completions,  goal 10
        self.insert_daily_habit_w_streak()

        #loading the habits
        self.hc.load_habits()

        # select the habit
        habit = self.hc.habits[0]


        #this must result in 50 (50%)
        true_completion_rate = (5/10)*100

        test_completion_rate = (habit.completed_reps/habit.goal_count)*100

        #asserting the values
        assert true_completion_rate == habit.completion_ratio

        assert  test_completion_rate == habit.completion_ratio




    #~~~~~~~~~~~~~~~~~~~~~~ MANIPULATION MODULE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



    # ~~~~~~Add_habits()~~~~~~~~~~

    #testing priority:

    #1) goal_count must be a positive integer
    #2) no name duplicates allowed
    #3) name can not be empty
    #4) Custom habits get assigned correct interval



    #1) goal count must be positive integer

    # first test for negative number
    def test_add_habit_goal_negative_number(self):

        # checking for an exception if the number is negative:

        with pytest.raises(ValueError):
            self.hc.add_habit("Reading", "2 hours of reading", "weekly", -1)

    # second for a string input
    def test_add_habit_goal_string(self):

        # checking for an exception if the goal set is a word
        with pytest.raises(ValueError):
            self.hc.add_habit("Reading", "2 hours of reading", "weekly", "wrong input")

    # third for an empty input
    def test_add_habit_goal_empty(self):

        # checking for an exception if the number is negative:

        with pytest.raises(ValueError):
            self.hc.add_habit("Reading", "2 hours of reading", "weekly",None)



    #2) Duplicate name test

    def test_add_habit_duplicate_name(self):

        #trying to insert the same habit twice

        self.hc.add_habit("Reading", "2 hours of reading", "weekly", 20)

        #checking for exception

        with pytest.raises(ValueError):
            self.hc.add_habit("Reading", "2 hours of reading", "weekly", 20)


    #3) No name
    def test_add_habit_empty_name(self):

        #checking for exception

        with pytest.raises(ValueError):
            self.hc.add_habit("", "2 hours of reading", "weekly", 20)


    #4) Custom habit interval assignment


    # No interval specified
    def test_add_habit_custom_habit(self):

        #checking for an exception
        # interval is set to none

        with pytest.raises(ValueError):
            self.hc.add_habit("Reading", "2 hours of reading", "custom", 20, None)


    # Check whether the interval is correct

    def test_add_habit_correct_interval(self):

        # the interval_set variable is set to 4

        self.hc.add_habit("Reading", "2 hours of reading", "custom", 20, 4)

        # select the habit
        habit = self.hc.habits[0]


        # asserting whether the interval was correctly assigned to 4
        assert habit.set_interval == 4



    # ~~~~~~Add_habits()~~~~~~~~~~

    # ~~~~~~Mark_today()~~~~~~~~~~

    #1) No double completions for a day
    #2) correct assignment of completed days


    #1) Double completions

    def test_mark_today_double_completions(self):

        #inserting a test habit
        self.hc.add_habit("Reading", "2 hours of reading", "custom", 20, 4)


        #completing the habit for today

        self.hc.mark_today("reading")

        with pytest.raises(ValueError):
            self.hc.mark_today("reading")


    #2) Correct completion date

    def test_mark_today_correct_date(self):

        # inserting a test habit
        self.hc.add_habit("Reading", "2 hours of reading", "custom", 20, 4)


        # completing the habit
        self.hc.mark_today("reading")

        # assigning today's date to a list
        check_today = [date.today()]

        #selecting the created habit
        habit = self.hc.habits[0]

        #asserting whether the completion date is in the list
        assert habit.completion_dates == check_today

        # ~~~~~~Mark_today()~~~~~~~~~~




    # ~~~~~~Reset_today()~~~~~~~~~~

    # Testing for:
    #1) Resetting today's completion with no completion = error
    #2) Correct deletion of a today's completion date


    #1) No completion

    def test_reset_today_no_completion(self):

        # inserting a test habit
        self.hc.add_habit("Reading", "2 hours of reading", "custom", 20, 4)

        # asserting that resetting results in exception

        with pytest.raises(ValueError):
            self.hc.reset_today("reading")


    #2) Correct deletion of completion

    def test_reset_today_correct_reset(self):

        # inserting a test habit
        self.hc.add_habit("Reading", "2 hours of reading", "custom", 20, 4)

        # completing the habit
        self.hc.mark_today("reading")

        # assigning today's date to a list
        check_today = [date.today()]

        # selecting the created habit
        habit = self.hc.habits[0]

        # asserting whether the completion date is in the list
        assert habit.completion_dates == check_today

        #remove the completion and assert for an empty list

        self.hc.reset_today("reading")

        assert habit.completion_dates == []

    # ~~~~~~Reset_today()~~~~~~~~~~



    # ~~~~~~Mark_habit_Date()~~~~~~~~~~

    #Test for:
    #1) Double completion results in exception
    #2) Correct mark  procedure

    #1) Double completion

    def test_mark_habit_date_double_completion(self):

        # inserting a habit with a shifted creation date, by 35 days, name - "running"

        self.insert_weekly_habit_no_completions()


        #adding the habit to local environment
        self.hc.load_habits()


        # completion date is 5 days from today
        completion_date = date.today() - timedelta(days=5)

        # marking once
        self.hc.mark_habit_date("Running", completion_date)

        # expecting an exception
        with pytest.raises(ValueError):
            self.hc.mark_habit_date("Running", completion_date)


    def test_mark_habit_date_correct(self):
        # inserting a habit with a shifted creation date, by 35 days, name - "running"

        self.insert_weekly_habit_no_completions()

        # adding the habit to local environment
        self.hc.load_habits()

        # completion date is 5 days from today
        completion_date = date.today() - timedelta(days=5)

        # selecting the created habit
        habit = self.hc.habits[0]

        #asserting no completions
        assert habit.completion_dates == []

        # marking once
        self.hc.mark_habit_date("Running", completion_date)

        #asserting the habit now contains the completion in a list form
        assert habit.completion_dates == [completion_date]

    # ~~~~~~Mark_habit_Date()~~~~~~~~~~


    # ~~~~~~Reset_completion()~~~~~~~~~~

    # Testing for:
    # Correct reset

    def test_reset_completion_no_completion(self):
        # inserting a habit with a shifted creation date, by 35 days, name - "running"

        self.insert_weekly_habit_no_completions()

        # adding the habit to local environment
        self.hc.load_habits()

        # completion date is 5 days from today
        completion_date = date.today() - timedelta(days=5)

        # selecting the created habit
        habit = self.hc.habits[0]

        # asserting no completions
        assert habit.completion_dates == []

        # marking once
        self.hc.mark_habit_date("Running", completion_date)

        # asserting the habit now contains the completion in a list form
        assert habit.completion_dates == [completion_date]

        #removing completion
        self.hc.reset_completion("Running", completion_date)

        # asserting for an empty list again
        assert habit.completion_dates == []

    # ~~~~~~Reset_completion()~~~~~~~~~~



    # ~~~~~~Reset_counter()~~~~~~~~~~

    # Testing for:

    # Correct procedure - removes all completions and, missed dates and sets the creation date to today

    def test_reset_counter_correct_deletion(self):

        #inserting a habit
        # reading  - current streak = 3, best streak = 3,  5 completions, 6 days missed, creation date = 10 days from today

        self.insert_daily_habit_w_streak()

        #load habit into local environment
        self.hc.load_habits()

        habit = self.hc.habits[0]

        today = date.today()

        #asserting the creation date and total completions and total missed

        creation_date = date.today() - timedelta(days=10)

        assert habit.creation_date == creation_date
        assert habit.completed_reps == 5
        assert habit.completions_missed == 6

        #resetting the habit
        self.hc.reset_counter("Reading")

        assert habit.creation_date == today
        assert habit.completed_reps == 0

        #asserting for 1, because daily habit starts with a missed completion,
        #due to the nature of set_interval variable
        assert habit.completions_missed == 1

    # ~~~~~~Reset_counter()~~~~~~~~~~


    # ~~~~~~Rename_habit()~~~~~~~~~~
    #check for correct procedure

    def test_rename_habit_correct(self):
        #insert a habit
        self.hc.add_habit("unnamed habit", "", "weekly",20)

        #select the habit
        habit = self.hc.habits[0]

        #assert the name
        assert habit.name == "unnamed habit"

        #rename the habit
        self.hc.rename_habit("unnamed habit", "renamed habit")

        # assert whether the name was changed
        assert habit.name == "renamed habit"

    # ~~~~~~Rename_habit()~~~~~~~~~~


    # ~~~~~~Change_description()~~~~~~~~~~
    # check for correct procedure

    def test_change_description(self):

        # insert a habit
        self.hc.add_habit("unnamed habit", "old description", "weekly", 20)

        # select the habit
        habit = self.hc.habits[0]

        # assert the name
        assert habit.description == "old description"

        # rename the habit
        self.hc.change_description("unnamed habit", "new description")

        # assert whether the name was changed
        assert habit.description == "new description"

    # ~~~~~~Change_description()~~~~~~~~~~



    # ~~~~~~Delete_habit()~~~~~~~~~~
    # check for correct procedure

    def test_delete_habit(self):

        # insert two habits for testing
        self.hc.add_habit("unnamed habit", "old description", "weekly", 20)
        self.hc.add_habit("reading", "book", "weekly", 10)



        # two habits must ocupy the local environment
        assert len(self.hc.habits) == 2

        # delete the habit
        self.hc.delete_habit("unnamed habit")

        # assert if a habit was deleted
        assert len(self.hc.habits) == 1

        #select the non-deleted habit
        habit = self.hc.habits[0]

        # assert that the habit of interest was deleted
        assert habit.name == "reading"

    # ~~~~~~Delete_habit()~~~~~~~~~~



    # STATISTICS FOR C-TKINTER IN HC MODULE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #~~~~~~~Best_habit()~~~~~~~~~~~~~

    def test_best_habit(self):
        # for testing, insert two habits.

        # reading score  = 46.81
        # running score  = 58.5   <- best habit


        # reading  - current streak = 3, best streak = 3,  5 completions, 6 days missed, goal set =10
        self.insert_daily_habit_w_streak()


        # ~~~~~~~~ Running -  5 completions, best streak =3 , current streak =3, missed = 3, goal set =10
        self.insert_weekly_habit_w_streak()

        #load the habits into local environment

        self.hc.load_habits()

        #selecting the running habit
        habit = self.hc.habits[1]

        running_score = habit.completion_ratio* 0.3 + habit.consistency_ratio*0.7

        true_running_score = ((5/10)*100) *0.3 + ((5/8)*100) * 0.7


        # retrieving the best habit
        best_name, best_score = self.hc.best_habit()

        #asserting the values
        assert best_name == habit.name
        assert best_score == running_score
        assert best_score == true_running_score

    # ~~~~~~~Best_habit()~~~~~~~~~~~~~


    # ~~~~~~~Worst_habit()~~~~~~~~~~~~~

    def test_worst_habit(self):
        # for testing, insert two habits.

        # reading score  = 46.81  <- worst habit
        # running score  = 58.5

        # reading  - current streak = 3, best streak = 3,  5 completions, 6 days missed, goal set =10
        self.insert_daily_habit_w_streak()

        # ~~~~~~~~ Running -  5 completions, best streak =3 , current streak =3, missed = 3, goal set =10
        self.insert_weekly_habit_w_streak()

        # load the habits into local environment

        self.hc.load_habits()

        # selecting the reading habit
        habit = self.hc.habits[0]


        #calculating the scores of reading habit
        reading_score = habit.completion_ratio * 0.3 + habit.consistency_ratio * 0.7

        true_reading_score = ((5 / 10) * 100) * 0.3 + ((5 / 11) * 100) * 0.7

        #calling in the function
        worst_name , worst_score = self.hc.worst_habit()

        # asserting the results

        assert worst_name == habit.name
        assert worst_score == reading_score
        assert worst_score == true_reading_score

    # ~~~~~~~Worst_habit()~~~~~~~~~~~~~

    # ~~~~~~~Goal_percentage()~~~~~~~~~~~~~

    def test_goal_percentage(self):
        # for testing, insert two habits.

        # reading  - current streak = 3, best streak = 3,  5 completions, 6 days missed, goal set =10
        self.insert_daily_habit_w_streak()

        # ~~~~~~~~ Running -  5 completions, best streak =3 , current streak =3, missed = 3, goal set =10
        self.insert_weekly_habit_w_streak()

        #load the habits into local environment
        self.hc.load_habits()

        #calculating the goal percentage : (5+5)/(10+10) *100

        true_goal_percentage = (10/20) *100

        #call in the function
        goal_percentage = self.hc.goal_percentage()

        #asserting the values

        assert goal_percentage == true_goal_percentage

    # ~~~~~~~Goal_percentage()~~~~~~~~~~~~~



    # ~~~~~~~~~Current_best_streak()~~~~~~~~

    def test_current_best_streak(self):
        # insert two habits

        #best current streak habit:
        # reading  - current streak = 3, best streak = 3,  5 completions, 6 days missed, goal set =10
        self.insert_daily_habit_w_streak()

        #  Running -  2 completions, best streak =1 , current streak =0, missed
        self.insert_weekly_habit_completed()

        #load the habits
        self.hc.load_habits()

        habit = self.hc.habits[0]

        #initiate the function
        best_name, best_streak = self.hc.current_best_streak()

        #assert the values, if they match reading habit scores
        assert habit.current_streak == best_streak
        assert habit.name == best_name
        assert best_streak == 3

































































































































































































    def test_add_habit_all_types_ok(self):
        #create a list of habits to add:

        habit_list =[ ("Reading", "5mins", "daily", 5),("Running", "2km", "weekly", 10),
                  ("Meditation", "2 hours", "monthly", 5),("Vitamins", "", "custom", 5,9)]

        for i in habit_list:
            self.hc.add_habit(*i)

        assert len(self.hc.habits) == 4












    
        
        
        






