
from datetime import date, timedelta, datetime
from DB1 import DBHandler




# All habits must have three general parameters specified - habit name, description, and a number of goal number of repetitions
# Other parameters will be specified in subclasses
class Habit:
    def __init__(self,db_id, name, description, goal_count):
        self.db_id = db_id
        self.name = name
        self.description = description
        self.goal_count = goal_count
        self.set_interval = None
        self.completed_reps = 0
        self.completions_missed = 0
        self.is_completed = "In progress"
        self.reps_left = 0
        self.approximate_completion = None
        self.next_deadline = None
        self.current_streak = 0
        self.best_streak = 0
        self.last_completion = None
        self.creation_date = None
        self.completion_dates = []
        self.missed_dates = []
        self.performance_score = 0
        self.completion_ratio = 0
        self.consistency_ratio = 0


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Adds a completion and appends a completion date

    def calculate_completion_ratio(self):

        #no completions = 0
        if self.goal_count <= 0:
            self.completion_ratio = 0
            return self.completion_ratio

        #calculating the rates
        #setting the limit to 100 as maximum

        ratio = (self.completed_reps / self.goal_count) * 100
        ratio = min(ratio, 100)

        self.completion_ratio = ratio
        return ratio

    def calculate_consistency_ratio(self):
        total = self.completed_reps + self.completions_missed

        if total == 0:
            self.consistency_ratio = 0
            return 0

        ratio = (self.completed_reps / total) * 100
        self.consistency_ratio = ratio
        return ratio




    def calculate_performance_score(self):
        # calculates weighted mean for performance scores - consistency % alone is unreliable
        # 30% is made up by completion_% and 70% of consistency_%
        performance_score = self.completion_ratio * 0.3 + self.consistency_ratio * 0.7

        self.performance_score = performance_score


    # counts the total completed instances and how many repetitions are left until the goal
    def total_completed(self, db):
        self.completed_reps = db.total_completed_sql(self.db_id)
        self.reps_left = max(0, self.goal_count - self.completed_reps)
        self.is_completed = "Completed" if self.reps_left == 0 else "In progress"



    def calculate_dates(self):

        last_date = None

        if self.completion_dates:
            last_date = self.completion_dates[-1]
        else:
            last_date = self.creation_date - timedelta(1)


        reps_left = max(0, self.reps_left)
        # Recalculating the important dates using last completion date and habit type
        #accidentally broke the program, without setting exceptions if the date happens to be too large


        # not ideal, but I will allow the dates to become string, because they serve no purpose
        # other than to give some insight. But once completed, this is no longer needed
        if reps_left == 0:
            self.approximate_completion = "Goal achieved!"
            self.next_deadline = " - "

        else:

            try:
                self.approximate_completion = last_date + timedelta(days=reps_left * self.set_interval)
            except OverflowError:
                self.approximate_completion = date.max

            try:
                self.next_deadline = last_date + timedelta(days=self.set_interval)
            except OverflowError:
                self.next_deadline = date.max

    def streak(self, db):

        self.creation_date = db.fetch_creation_date_sql(self.db_id)
        #Date calculation if there are no completions
        # we compare today's date with the creation day
        completed_dates = sorted(db.fetch_completion_dates_sql(self.db_id))

        if not completed_dates:
            missed_dates = set()
            today = date.today()


            gap = (today - self.creation_date).days

            # we add 1, in order to include the creation date in the interval
            total_missed = (gap + 1)   // self.set_interval

            #inserting the missed date  manually to include creation date in the interval
            missed_creation_date = self.creation_date + timedelta((self.set_interval -1))

            missed_dates.add(missed_creation_date)

            #reducing the total number, since once record was added manually





            # adding missed dates normally
            for i in range(1, total_missed):
                missed_date = missed_creation_date + timedelta(days=i * self.set_interval)
                missed_dates.add(missed_date)

            self.completions_missed = total_missed
            self.current_streak = 0
            self.best_streak = 0
            self.last_completion = None
            self.completion_dates = []
            self.missed_dates = missed_dates
            return
        # date and streak calculations with completion dates
        self.completion_dates = completed_dates
        best_streak = 0
        current_streak = 0
        last_completion = None
        total_missed = 0
        missed_dates = set()


        #first we calculate the gap between creation date and first completion, this will not be included in the upcoming loop
        first_completion = completed_dates[0]

        gap = (first_completion - self.creation_date).days
        missed_3 = max(0,  gap // self.set_interval)

        #adds completions
        total_missed += missed_3

        # finds the missed dates between first completion and the creation date

        # we use self.set_interval -1, so the missed dates start from the creation date
        for i in range(1,missed_3 +1):
            missed_date = self.creation_date +timedelta(days=i * self.set_interval -1 )
            missed_dates.add(missed_date)


        # the complete timelapse = 1) from creation date to first completion 2) from first completion to last completion 3) from last completion until today



        # The for loop checks whether each individual completed date was completed within the bounds of the interval set (f.e. "monthly" or "every n days", the user has set
        # it starts by setting the last_completion to value "None" and last_completion will always be replaced with the completed date, that was already checked
        # Therefore, it always compares two completion dates - one (recent) with the completion date before that
        # Then it calculates the distance between the dates and compares with the interval_set. If the completion dates are fall outside the interval - it calculates
        # how many times the user missed to complete the habit
        for i in completed_dates:
            if last_completion is None:
                current_streak = 1
            else:
                gap_between_completions = (i - last_completion).days
                missed = max(0, (gap_between_completions - 1) // self.set_interval)

                if missed > 0:
                    for j in range(1,missed +1):
                        missed_date = last_completion + timedelta(days=j * self.set_interval)
                        missed_dates.add(missed_date)

                total_missed += missed

                # breaks the streak
                if missed > 0:
                    current_streak = 1
                else:
                    current_streak += 1

            best_streak = max(best_streak, current_streak)
            last_completion = i

            # for loop sets this variable to the completion date (previous),
            # that will be checked with the next one.
            # save the data

        # However, the last completion still needs to be checked with the date of today,
        # in case, the person did not complete the habit
        today = date.today()
        gap = (today - last_completion).days

        missed_2 = max(0, gap // self.set_interval)
        if missed_2 > 0:
            current_streak = 0


        #loop that appends the missed dates
        if missed_2 > 0:
            for j in range(1, missed_2 + 1):
                missed_date = last_completion + timedelta(days=j * self.set_interval)
                missed_dates.add(missed_date)

        total_missed += missed_2

        self.best_streak = best_streak
        self.current_streak = current_streak
        self.completions_missed = total_missed
        self.last_completion = last_completion

        #will be used for filtering by year, month

        self.missed_dates = missed_dates




                # Four subclasses available - daily, weekly, monthly and custom (user must specify preferred interval)
class DailyHabit(Habit):
    def __init__(self, db_id, name, description, goal_count):
        super().__init__(db_id, name, description, goal_count)
        self.habit_type = "daily"
        self.set_interval = 1

class WeeklyHabit(Habit):
    def __init__(self, db_id, name, description, goal_count):
            super().__init__(db_id, name, description, goal_count)
            self.habit_type = "weekly"
            self.set_interval = 7

class MonthlyHabit(Habit):
    def __init__(self, db_id, name, description, goal_count):
        super().__init__(db_id, name, description, goal_count)
        self.habit_type = "monthly"
        self.set_interval = 30

class CustomHabit(Habit):
    def __init__(self, db_id, name, description, goal_count, set_interval):
        super().__init__(db_id, name, description, goal_count)
        self.habit_type = "custom"
        self.set_interval = set_interval



class HabitControl:
    def __init__(self, dh: DBHandler):
        self.habits = []
        self.dh = dh




    def list_all_by_type(self, habit_class):
        return [i.name for i in self.habits if i.habit_type == habit_class]

    def list_all_habits(self):
        return [i.name for i in self.habits]

    def add_habit(self, name, description, habit_type, goal_count, set_interval=None):
        # ~~~ lowercases habit type for consistency
        if habit_type:
            habit_type = habit_type.lower().strip()

        # ~~~~ checks name and duplicate name
        if not name:
            raise ValueError("Name cannot be empty!")
        else:
            name = name.lower()

        name_check = self.dh.check_name_sql(name)
        if name_check:
            raise ValueError("Such habit already exists!")

        # ~~~~~~ checks goal repetitions are positive integer

        if goal_count == None:
            raise ValueError("Please enter your goal number of repetitions!")

        try:
            goal_count = int(goal_count)
        except ValueError:
            raise ValueError("Goal repetitions must be a number!")

        if goal_count <= 0:
            raise ValueError("Goal repetitions must be a positive integer!")

        # ~~~~ checks if custom interval exists, is positive integer

        if habit_type == "custom":
            if set_interval is None:
                raise ValueError("Specify the custom interval!")

            try:
                set_interval = int(set_interval)
            except ValueError:
                raise ValueError("Custom interval must be a number!")

            if set_interval <= 0:
                raise ValueError("Custom interval must be a positive integer!")

        # The record is created in the habits table (SQL)
        db_id = self.dh.insert_habit_sql(name, description, habit_type, set_interval, goal_count)

        # additionally the habit is instantly saved locally
        if habit_type == "daily":
            habit = DailyHabit(db_id, name, description, goal_count)
        elif habit_type == "weekly":
            habit = WeeklyHabit(db_id, name, description, goal_count)
        elif habit_type == "monthly":
            habit = MonthlyHabit(db_id, name, description, goal_count)
        else:
            habit = CustomHabit(db_id, name, description, goal_count, set_interval)

        # Saves the habits locally
        self.habits.append(habit)
        self.refresh_habits()


    def mark_today(self,user_chosen):
        habit = next(i for i in self.habits if i.name == user_chosen)
        mark_date = date.today()

        last_completion= self.dh.get_last_completion_date_sql(habit.db_id)

        if mark_date == last_completion:
            raise ValueError ("The habit was already completed today!")


        marked_habit = self.dh.mark_habit_sql(habit.db_id, mark_date)

        if not marked_habit:
            raise ValueError("The habit was already completed today!")

        self.refresh_habits()



    def mark_habit_date(self,user_chosen,mark_date):
        habit = next(i for i in self.habits if i.name == user_chosen)
        all_completion_dates = self.dh.fetch_completion_dates_sql(habit.db_id)

        if mark_date in all_completion_dates:
            raise ValueError("The habit is already completed for that day!")

        marked_habit = self.dh.mark_habit_sql(habit.db_id, mark_date)

        if marked_habit:
            habit.completion_dates.append(mark_date)

        self.refresh_habits()




    def reset_today(self, user_chosen):

        habit = next((i for i in self.habits if i.name == user_chosen), None)

        if habit is None:
            raise ValueError(f"Habit '{user_chosen}' does not exist.")

        #fetching the today completed habits from the mark_table
        completion_id = self.dh.fetch_today_completed_id_sql()

        #if the id's dont match - > error
        if habit.db_id not in completion_id:
            raise ValueError(f"the habit '{habit.name.capitalize()}' was not completed today")

        # deletes the completion from the database
        self.dh.reset_todays_completion_sql(habit.db_id)

        #removes the completion locally
        habit.completion_dates.remove(date.today())

        #updates the local data
        if habit.completed_reps > 0:
            habit.completed_reps -= 1
            habit.reps_left += 1

        self.refresh_habits()


    def reset_completion(self, user_chosen,chosen_date):

        habit = next((i for i in self.habits if i.name == user_chosen), None)

        if habit is None:
            raise ValueError(f"Habit '{user_chosen}' does not exist.")


        # deletes the completion from the database
        self.dh.reset_completion_sql(habit.db_id,chosen_date)

        #updates the local data
        if habit.completed_reps > 0:
            habit.completed_reps -= 1
            habit.reps_left += 1

            #remove the completion date
            if chosen_date in habit.completion_dates:
                habit.completion_dates.remove(chosen_date)


        self.refresh_habits()






    def reset_counter(self, user_chosen):

        habit = next((i for i in self.habits if i.name == user_chosen), None)

        if habit is None:
            raise ValueError(f"Habit '{user_chosen}' does not exist.")


        #deletes all the data in the mark table
        self.dh.reset_records_sql(habit.db_id)

        #resets the creation date to today
        self.dh.reset_creation_date_sql(habit.db_id)

        habit.is_completed = "In progress"
        habit.completed_reps = 0
        habit.reps_left = habit.goal_count
        habit.creation_date = date.today()
        habit.completion_dates = []
        habit.missed_dates = []
        self.refresh_habits()



    def calendar_dates(self,user_chosen):
        habit = next(i for i in self.habits if i.name == user_chosen)

        # will be displayed in violet
        creation_date = self.dh.fetch_creation_date_sql(habit.db_id)
        completion_dates = []

        #will be displayed in green
        completion_dates = self.dh.fetch_completion_dates_sql(habit.db_id)

        # calendar will only contain the dates from completion date until today
        check = date.today() - creation_date

        all_dates = [creation_date+ timedelta(days=i) for i in range(check.days+1)]

        return creation_date, completion_dates, all_dates




    def rename_habit(self, user_chosen, new_name):
        habit = next((i for i in self.habits if i.name == user_chosen), None)
        if habit is None:
            raise ValueError(f"Habit '{user_chosen}' does not exist.")

        check = next((i for i in self.habits if i.name == new_name), None)
        if check:
            raise ValueError (f"Habit '{new_name.capitalize()}' already exists! Try a different name.")


        self.dh.rename_habit_sql(habit.db_id, new_name)

        #save locally
        habit.name = new_name




    def change_description(self,user_chosen,new_description):
        habit = next((i for i in self.habits if i.name == user_chosen), None)

        if habit is None:
            raise ValueError(f"Habit '{user_chosen}' does not exist.")

        #update database
        self.dh.change_description_sql(habit.db_id, new_description)

        #update locally
        habit.description = new_description





    def delete_habit(self, user_chosen):
        habit = next((i for i in self.habits if i.name == user_chosen), None)

        if habit is None:
            raise ValueError(f"Habit '{user_chosen}' does not exist.")


        #remove from the database
        self.dh.delete_habit_sql(habit.db_id)

        #remove locally
        self.habits.remove(habit)



    # this function will load the data from the database into local environment
    def load_habits(self):
        self.dh.create_tables_sql()

        #makes sure the local data is empty before proceeding
        self.habits.clear()
        rows = self.dh.fetch_all_habits_sql()

        for i in rows:
            db_id, name, description, habit_type, set_interval, goal_count, creation_date = i

            # Instantiate the correct subclass
            if habit_type == "daily":
                habit = DailyHabit(db_id, name, description, goal_count)
            elif habit_type == "weekly":
                habit = WeeklyHabit(db_id, name, description, goal_count)
            elif habit_type == "monthly":
                habit = MonthlyHabit(db_id, name, description, goal_count)
            elif habit_type == "custom":
                habit = CustomHabit(db_id, name, description, goal_count,set_interval)
            else:
                continue
            habit.creation_date = creation_date

            self.habits.append(habit)
            self.refresh_habits()



    def exit_application(self):
        self.dh.close_application_sql()
        exit()


    def refresh_habits(self):
        #recalculates the statistics
        for habit in self.habits:
            habit.total_completed(self.dh)
            habit.streak(self.dh)
            habit.calculate_dates()

            habit.calculate_consistency_ratio()
            habit.calculate_completion_ratio()
            habit.calculate_performance_score()




    # STATISTICS FOR C-TKINTER~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def filter_habits(self, time_filter, type_filter, chosen_date):
        sorted_habits = self.habits

        if type_filter.lower() != "all":
            sorted_habits = [i for i in sorted_habits if i.habit_type.lower() == type_filter.lower()]


        missed_dates_fn = {}
        completed_dates = {}



        # Loop out the  missed and the dates of completions that are within the specified month/year
        # The function assigns each date its total number of completions in form of a dictionary
        # using the get function we set the date as key and its default alue to 0

        if time_filter == "Lifetime":
            for i in sorted_habits:
                for j in i.completion_dates:
                        completed_dates[j] = completed_dates.get(j,0) + 1

            for i in sorted_habits:
                for j in i.missed_dates:
                        missed_dates_fn[j] =  missed_dates_fn.get(j,0) +1


        if time_filter == "Yearly":
            for i in sorted_habits:
                for j in i.completion_dates:
                    if j.year == chosen_date.year:
                        completed_dates[j] = completed_dates.get(j,0) + 1


            for i in sorted_habits:
                for j in i.missed_dates:
                    if j.year == chosen_date.year:
                        missed_dates_fn[j] =  missed_dates_fn.get(j,0) +1


        if time_filter == "Monthly":
            for i in sorted_habits:
                for j in i.completion_dates:
                    if j.year == chosen_date.year and j.month == chosen_date.month:
                        completed_dates[j] = completed_dates.get(j,0) + 1


            for i in sorted_habits:
                for j in i.missed_dates:
                    if j.year == chosen_date.year and j.month == chosen_date.month:
                        missed_dates_fn[j] =  missed_dates_fn.get(j,0) + 1


        return sorted_habits, completed_dates, missed_dates_fn



    def count_habits(self):
        return len(self.habits)



    def totals_sorted(self, time_filter, type_filter, chosen_date):
        sorted_habits, completions_date, missed_dates = self.filter_habits(time_filter, type_filter, chosen_date)

        # count the total missed and completed dates, for the pie chart
        total_completions = sum(completions_date.values())
        total_missed = sum(missed_dates.values())

        total = total_completions+ total_missed

        if total ==0:
            total_consistency = 0
        else:
            total_consistency = (total_completions/total) *100
            total_consistency = round(total_consistency, 1)

        return total_missed, total_completions, total_consistency


    def goal_percentage(self):

        total_goal_count = sum(i.goal_count for i in self.habits)
        total_reps_left = sum(i.reps_left for i in self.habits)


        if total_goal_count == 0:
            return 0
        return (total_goal_count - total_reps_left) / total_goal_count * 100

    def worst_habit(self):
        if not self.habits:
            return None

        worst_name = "No habit data"
        worst_score = 0

        for i in self.habits:
            if worst_score == 0 or i.performance_score < worst_score:
                worst_score = i.performance_score
                worst_name = i.name

        return worst_name, worst_score

    def best_habit(self):

        best_name = "No habit data"
        best_score = 0

        if not self.habits:
            return best_name, best_score


        for i in self.habits:
            if best_score == 0 or i.performance_score > best_score:
                best_score = i.performance_score
                best_name = i.name.capitalize()

        return best_name, best_score

    def current_best_streak(self):
        current_best_habit = "No data"
        current_best_streak = 0

        if not self.habits:
            return current_best_habit,current_best_streak


        for i in self.habits:
            if current_best_streak == 0 or i.current_streak > current_best_streak:
                current_best_streak = i.current_streak
                current_best_habit = i.name.capitalize()

        return current_best_habit, current_best_streak







