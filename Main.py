from customtkinter import *
from CTkMessagebox import CTkMessagebox
from operator import itemgetter, attrgetter
from DB1 import DBHandler
from Habits import HabitControl
from datetime import date, timedelta, datetime
import calendar
from graphs import Graphs
from tkinter import *
from tkcalendar import Calendar



set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("themes/coffee.json")

class App(CTk):
    def __init__(self):
        super().__init__()
        dh = DBHandler("DB1.db")
        self.hc = HabitControl(dh)
        self.hc.load_habits()
        self.gr =Graphs()


        #variables that will be used for calendar manipulation later on
        self.selected_calendar_date = None
        self.selected_habit = None
        self.shown_date = None


        #~~~~~~~~~~ general dimensions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.geometry("1250x750")
        self.title("Habit Tracker!")

        #~~~~~~~~~~~~~Main Menu frame~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        self.main_menu_frame = CTkFrame(self, width = 200)
        self.main_menu_frame.grid(row=0, column= 0, sticky = "ns")

        title = CTkLabel(self.main_menu_frame, text = "Main Menu", font = CTkFont(family = "arial",weight = "bold", size = 60))
        title.grid(row=0, column = 0, pady= 20, padx = 10)


        #~~~~~~~~~~~~~~~~~ Grid configuration (stretch mode)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """The menu bar should stay the same size (takes col 0 and row 0)  and the function display can be expanded or subtracted (col 1 and row 0)"""

        self.grid_columnconfigure(0, weight = 0)  #Menu bar - fixed
        self.grid_columnconfigure(1,weight=1) # Content display  - expandable



        # ~~~~~~~~~~~~~~~~~~~~~~ Main Menu Buttons~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.btn_complete = CTkButton(self.main_menu_frame, text="Complete Habit", font= CTkFont(family = "arial",weight = "bold", size = 15), corner_radius= 32, command =self.complete_habit_tk)
        self.btn_create = CTkButton(self.main_menu_frame, text="Create a new Habit" ,font= CTkFont(family = "arial",weight = "bold", size = 15), corner_radius= 32, command = self.create_habit_tk )
        self.btn_analyse = CTkButton(self.main_menu_frame, text="Analyse Habit",font= CTkFont(family = "arial",weight = "bold", size = 15), corner_radius= 32, command = self.analyse_habit)
        self.btn_performance = CTkButton(self.main_menu_frame, text="Habit Statistics",font= CTkFont(family = "arial",weight = "bold", size = 15), corner_radius= 32 , command = self.habits_statistics )
        self.btn_modify = CTkButton(self.main_menu_frame, text="Modify Habits",font= CTkFont(family = "arial",weight = "bold", size = 15), corner_radius= 32,command= self.modify_habit)
        self.btn_exit = CTkButton(self.main_menu_frame, text="Save And Exit",font= CTkFont(family = "arial",weight = "bold", size = 15), corner_radius= 32, command = self.save_and_exit)



        buttons = [self.btn_complete, self.btn_create, self.btn_analyse,
                self.btn_performance, self.btn_modify, self.btn_exit]

        for i, btn in enumerate(buttons, start=1):
            btn.grid(row=i, column=0, pady=10, padx=20, sticky="ew")
            #cool loop, each button gets its row assigned, Main menu gets 0 row.

        #~~~~~~~~~~~~~~~~~~ Content Display (second display)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.content_display = CTkFrame(self)
        self.content_display.grid(row= 0 , column = 1, sticky = "nsew")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)




        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN MENU FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear_screen_tk(self):
        for i in self.content_display.winfo_children():
            i.destroy()

    def reset_grid(self):
        # Get current grid size
        cols = self.content_display.grid_size()[0]
        rows = self.content_display.grid_size()[1]

        # Reset columns
        for c in range(cols):
            self.content_display.grid_columnconfigure(c, weight=0, minsize=0)

        # Reset rows
        for r in range(rows):
            self.content_display.grid_rowconfigure(r, weight=0, minsize=0)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE A NEW HABIT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_habit_tk(self):
        self.clear_screen_tk()
        self.reset_grid()

        def toggle_custom_interval():
            if habit_category.get().lower() == "custom":
                custom_label.grid(row =1, column = 1)
                custom_e.grid(row = 2, column = 1)
            else:
                custom_label.grid_forget()
                custom_e.grid_forget()


        def instruction_popup():
            popup = CTkToplevel(self)
            popup.title("Instructions")
            popup.geometry("600x300")

            popup.transient(self)
            instruction_text = ("To create a habit enter its name and description. \n\n"
            "Enter your goal - a desired number of habit repetitions. F.e. 'I will read, every night for 30 days.' 30 days is you goal.\n\n"
            "Lastly select how often the habit should be performed - f.e. 'daily', 'weekly'.\n\n"
            "You can customize this interval by selecting custom category and typing in the interval in days\n\n"
            "f.e. if custom is set to  3 - then the habit should be repeated every 3 days.")




            instruction_text_box = CTkTextbox(popup, width=500, height=300,
                                              font=CTkFont(family="Arial", size=14, weight="bold"))
            instruction_text_box.insert("0.0", instruction_text)
            instruction_text_box.configure(state="disabled")
            instruction_text_box.pack()


        def submit_habit():
            name = name_e.get().strip()
            description = description_e.get("0.0", "end").strip()
            goal_count = reps_e.get()
            habit_type = habit_category.get().lower()
            set_interval = custom_e.get().strip() if habit_type == "custom" else None

            try:
                self.hc.add_habit(name,description,habit_type, goal_count,set_interval)
                CTkMessagebox(title= "Success", message = "The habit was successfully added!", icon = "check")
            except ValueError as error:
                CTkMessagebox(title = "Error", message= str(error), icon = "warning")

            return


        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Frames

        # reset configuration, because some menu options ruins the design


        self.creation_frame = CTkFrame(self.content_display)
        self.creation_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=20)

        self.creation_frame.grid_columnconfigure(0,weight = 2, minsize= 300)
        self.creation_frame.grid_columnconfigure(1, weight=1, minsize=260)

        self.content_display.grid_columnconfigure(0, weight=2)
        self.content_display.grid_columnconfigure(1, weight=1)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Title and labels
        title = CTkLabel(self.creation_frame, text="Create a new habit",
                         font=CTkFont(family="arial", size=25, weight="bold"))
        title.grid(column=0, row=0, pady=12, padx=5, sticky = "nw")

        prompt_label= CTkLabel(self.creation_frame, text="Enter the following information:",
                         font=CTkFont(family="arial", size=17, weight="bold"))
        prompt_label.grid(column=0, row=1, pady=5, padx=10, sticky = "nw")

        description_label = CTkLabel(self.creation_frame, text = "Enter habit's description:",
                                     font=CTkFont(family="arial", size=15, weight="bold", ))
        description_label.grid(column = 0, row = 7 , pady= 8, padx=10, sticky = "nw")

        type_label = CTkLabel(self.creation_frame, text="Select your habit type:",
                         font=CTkFont(family="arial", size=15, weight="bold"))
        type_label.grid(column=0, row=5, pady=5, padx=10, sticky = "nw")

        custom_label= CTkLabel(self.creation_frame, padx= 20, text="Repeat habit every 'Nth' days:",
                         font=CTkFont(family="arial", size=15, weight="bold"))


        #~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Entry boxes
        name_e = CTkEntry(self.creation_frame, placeholder_text="Habit Name", height = 50)
        name_e.grid( column = 0, row=2, padx= 8, pady= 5,sticky = "ew")

        description_e = CTkTextbox(self.creation_frame,width= 300, height = 200, font = CTkFont(family ="Arial", size= 14))
        description_e.grid(column = 0, row=8, padx=10, pady=20,sticky = "ew")

        reps_e = CTkEntry(self.creation_frame, placeholder_text="Goal Repetitions", height= 50)
        reps_e.grid(column = 0, row=3, padx=8, pady=5 ,sticky = "ew")

        custom_e = CTkEntry(self.creation_frame, placeholder_text="Interval in days", height= 50)


        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Habit Category toggle switch categories
        habit_category = StringVar(value="Daily")
        habit_category_options = CTkOptionMenu(self.creation_frame, variable=habit_category, values=["Daily", "Weekly", "Monthly", "Custom"],
                                font=CTkFont(family="arial", size=13, weight="bold"),
                                command=lambda x: toggle_custom_interval())

        habit_category_options.grid(row=6, column=0, pady=10)


        #~~~~~~~~~~~~~ Buttons for instructions and submitting


        instruction_btn  = CTkButton(self.creation_frame, text="Instructions",
                                  font=CTkFont(family="arial", weight="bold", size=15), corner_radius=32, command = instruction_popup )
        add_btn = CTkButton(self.creation_frame, text="Add Habit",
                                    font=CTkFont(family="arial", weight="bold", size=15), corner_radius=32, command = submit_habit )

        instruction_btn.grid(column = 1, row = 7, padx = 20,sticky ="ew")
        add_btn.grid(column=1, row=8, padx= 20,sticky ="ew")

        #Setting the column (1st) size, because custom option function ruins the grid and starts jumping


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  CALENDAR  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    def calendar_completion_tk(self, habit, given_frame, on_date_click=None):

        # ~~~~~~~~~~~~~ Clear function
        if hasattr(self, "calendar_frame"):
            self.calendar_frame.destroy()

        if not hasattr(self, "selected_calendar_date"):
            self.selected_calendar_date = None

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Calendar Frame

        self.calendar_frame = CTkScrollableFrame(given_frame, label_text="Habit Calendar",
                                                 label_font=CTkFont(family="arial", weight="bold", size=15))
        self.calendar_frame.grid(row=7, column=0, columnspan=2, padx=12, pady=12, sticky="nsew")

        self.calendar_frame.grid_columnconfigure(0, weight=1)

        month_frame = CTkFrame(self.calendar_frame)
        month_frame.grid(row=0, column=0, columnspan=7, sticky="ew", pady=(0,10))


        #center the header, so its stop moving around like crazy
        month_frame.grid_columnconfigure(0, weight=1)
        month_frame.grid_columnconfigure(1, weight=0)
        month_frame.grid_columnconfigure(2, weight=1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Retrieving dates from habitcontrol

        creation_date, completion_dates, all_dates = self.hc.calendar_dates(habit)
        today = date.today()

        # ~~~~~~~~~~~~~~~~~~~~~~ toggling between dates - removes previously marked
        if not hasattr(self, "shown_date") or self.shown_date is None:
            self.shown_date = today.replace(day=1)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MONTHS CODE


        shown_date = self.shown_date

        #~~~~ Headers

        header = CTkLabel(month_frame, text=shown_date.strftime("%B %Y"),
                          font=CTkFont(family="arial", size=18, weight="bold"))
        header.grid(row=0, column=1, padx=5)

        #~~~~ Month navigation

        year = shown_date.year
        month = shown_date.month
        days_in_month = calendar.monthrange(year, month)[1]



        month_dates = [
            date(year, month, day)
            for day in range(1, days_in_month + 1)]
        month_dates = [i for i in month_dates if creation_date <= i <= today]



        def previous_month():
            month = shown_date.month -1
            year = shown_date.year
            if month == 0:
                month = 12
                year -= 1
            self.shown_date = shown_date.replace(year = year, month = month)
            self.calendar_completion_tk(habit,given_frame)

        def next_month():
            month = shown_date.month +1
            year = shown_date.year
            if month == 13:
                month = 1
                year += 1
            self.shown_date= shown_date.replace(year=year, month = month)
            self.calendar_completion_tk(habit,given_frame)



            #~~~~~~~~~~~~~~~~~~~~~~~ navigation buttons

        CTkButton(month_frame, text="◀", width=30, command=previous_month).grid(row=0, column=0, padx = 10, sticky = "w")

        CTkButton(month_frame, text="▶", width=30, command=next_month).grid(row=0, column=2, padx=10, sticky = "e")


        # ~~~~~~~~~~~~~~~~~~~~~~~ modifying the click on dates
        def click(date_clicked):
            self.selected_calendar_date = date_clicked

            if on_date_click:
                on_date_click(habit, date_clicked)
            else:
                self.calendar_completion_tk(habit, given_frame)



        # ~~~~~~~~~~~~~~~~~~~ Creating Calendar loop

        days_frame = CTkFrame(self.calendar_frame)
        days_frame.grid(row=1, column=0, columnspan=7, sticky="nsew")


        #allows the buttons to adjust when expanding the screen
        for col in range(7):
            days_frame.grid_columnconfigure(col, weight=1)


        for idx, i in enumerate(month_dates):

            # colours for completions and text colours to distinguish creation date and today
            if i < creation_date:
                continue

            if i > today:
                continue

            bg = "#f6f5f5"
            text_color = "#000000"

            if i in completion_dates:
                bg = "#1d902c"
            elif i == creation_date:
                text_color = "#744193"
            elif i == today:
                text_color = "#90241d"

            display_bg = "#268bb3" if getattr(self, "selected_calendar_date", None) == i else bg

            # ~~~~~~~~~~~~~ Dates come out as buttons

            buttons = CTkButton(days_frame, text=str(i.day),
                                fg_color=display_bg,
                                text_color=text_color, width=68, height=40,
                                command=lambda dc= i: click(dc))

            buttons.grid(row=(idx // 7) + 1, column=idx % 7, padx=4, pady=4)




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Filtering by type and displaying habits - used in combination with drop down
    def filter_and_display_habits_tk(self,habit_filter: str, given_frame, connected_function):
        for i in given_frame.winfo_children():
            i.destroy()

        if habit_filter.lower() == "all":
            filtered_habits = self.hc.habits
        else:
            filtered_habits = [i for i in self.hc.habits if i.habit_type.lower() == habit_filter.lower()]

        # sorts alphabetically
        sorted_habits = sorted(filtered_habits, key=attrgetter('name'))

        # creates buttons and numerates them and sends the selected habit to select_habit_tk() function

        for idx, i in enumerate(sorted_habits, start=1):
            habit = i
            CTkButton( given_frame,
                      text=f" {idx}.  {habit.name.capitalize()}",
                      font=CTkFont(family="arial", weight="bold", size=15),anchor= "w",
                      command=lambda h=habit: connected_function(h)
                      ).pack(pady=3, padx=5, fill="x")




        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  COMPLETE A HABIT  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def complete_habit_tk(self):
        shown_date = date.today().replace(day=1)

        self.clear_screen_tk()
        self.reset_grid()

        # ~~~~~~~~~~~~~~~~~~Frames

        self.select_frame = CTkScrollableFrame(self.content_display, label_text="Select a habit",
                                               label_font=CTkFont(family="arial", size=17, weight="bold"))
        self.select_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        self.options_frame = CTkFrame(self.content_display)
        self.options_frame.grid(row=1, column=1, sticky="nsew", padx=15, pady=10)

        for i in range(10):
            self.options_frame.grid_rowconfigure(i, weight=1)



        def calendar_helper_tk(habit):
            self.calendar_completion_tk(habit.name, self.options_frame)

        def complete_today(habit):
            try:
                self.hc.mark_today(habit.name)
                CTkMessagebox(title= "Success", message = "The habit was marked as completed for today!", icon = "check")

                calendar_helper_tk(habit)

            except ValueError as error:
                CTkMessagebox(title = "Error", message= str(error), icon = "warning")

            self.hc.refresh_habits()

        def complete_date(habit):
            if self.selected_calendar_date is None:
                CTkMessagebox(title="Error", message="Please select a date from the calendar!", icon="warning")
                return

            try:
                self.hc.mark_habit_date(habit.name, self.selected_calendar_date)
                CTkMessagebox(title="Success", message=f"The habit {habit.name} was marked as completed for {self.selected_calendar_date}!", icon="check")

                calendar_helper_tk(habit)



            except ValueError as error:
                CTkMessagebox(title = "Error", message= str(error), icon = "warning")

            self.hc.refresh_habits()





        #~~~~~~~~~~~~~~~~~~~~~~  FUNCTION - Displaying selected habit
        def show_selected_habit_tk(habit):

            self.selected_habit_label.configure(text=habit.name.capitalize())
            calendar_helper_tk(habit)

            complete_today_btn = CTkButton(self.options_frame, text="Complete for today",
                                     font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,height= 30,
                                           command=lambda: complete_today(habit))
            complete_today_btn.grid(row=8, column=0, padx=15, pady=15, columnspan=2, sticky="nsew")

            complete_date_btn = CTkButton(self.options_frame, text="Complete for a selected date",
                                           font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,height= 30,
                                                    command=lambda: complete_date(habit))
            complete_date_btn.grid(row=9, column=0, padx=15, pady=15, columnspan=2, sticky="nsew")


        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Filtering by type and displaying habits

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~ Drop down option menu
        self.filter_and_display_habits_tk("All", self.select_frame, show_selected_habit_tk)

        habit_filter = StringVar(value="All")
        habit_filter_options = CTkOptionMenu(self.options_frame,
                                             variable=habit_filter,
                                             font=CTkFont(family="arial", size=13, weight="bold"),
                                             values=["All", "Daily", "Weekly", "Monthly", "Custom"],
                                             command= lambda i: self.filter_and_display_habits_tk(i, self.select_frame, show_selected_habit_tk))

        habit_filter_options.grid(row=1, column=0, pady=10, padx=12, sticky="w")


        #~~~~~~~~~~~~~~~~~ frame/grid adjustments

        #  for selection display fixed and space for buttons, filters etc. is expandable

        #columns
        self.content_display.grid_columnconfigure(0,weight =0)
        self.content_display.grid_columnconfigure(1, weight=1)
        #rows
        self.content_display.grid_rowconfigure(1, weight =1)
        self.content_display.grid_rowconfigure(0, weight=0)

        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Title and labels

        #scrollframe label

        #title~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        title = CTkLabel(self.content_display, text="Complete Habit",
                         font=CTkFont(family="arial", size=25, weight="bold"))
        title.grid(column=0, row=0, pady=15, padx=15, sticky= "nw")



        #Filter label~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        label_1 = CTkLabel(self.options_frame, text = "Filter habits by category:",
                                font=CTkFont(family="arial", size=16, weight="bold"))
        label_1.grid(column=0, row=0, pady=8, padx=12, sticky = "w")

        label_2 = CTkLabel(self.options_frame, text="Your selected habit:",
                                font=CTkFont(family="arial", size=16, weight="bold"))
        label_2.grid(column=1, row=0, pady=8, padx=12, sticky="ew")

        self.selected_habit_label =CTkLabel(self.options_frame, text = "None",
                                 font=CTkFont(family="arial", size=20, weight="bold"), text_color= "#5d4511")
        self.selected_habit_label.grid(column=1, row=1, pady=15, padx=8, sticky="ew", columnspan =2)











#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def modify_habit(self):

        self.clear_screen_tk()
        self.reset_grid()

        # ~~~~~~~~~~~~~~~~~~Frames

        self.frame_1_modify = CTkScrollableFrame(self.content_display, label_text="Select a habit",  # the left screen
                                               label_font=CTkFont(family="arial", size=17, weight="bold"))
        self.frame_1_modify.grid(row=1, column=0, sticky="nsew", padx=15, pady=30)

        self.frame_2_modify = CTkFrame(self.content_display)  # the right screen
        self.frame_2_modify.grid(row=1, column=1, sticky="nsew", padx=15, pady=30)

        # columns
        self.content_display.grid_columnconfigure(0, weight=0)
        self.content_display.grid_columnconfigure(1, weight=1)
        # rows
        self.content_display.grid_rowconfigure(1, weight=1)
        self.content_display.grid_rowconfigure(0, weight=0)

        self.frame_2_modify.grid_columnconfigure(0, weight=1)
        self.frame_2_modify.grid_columnconfigure(1, weight=1)


        #adjusting the weights, forcing the buttons to adjust dimensions -> "nsew"
        for i in range(14):
            self.frame_2_modify.grid_rowconfigure(i, weight=1)

        # title~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        title = CTkLabel(self.content_display, text="Modify Habit",
                         font=CTkFont(family="arial", size=25, weight="bold"))
        title.grid(column=0, row=0, pady=15, padx=15, sticky="nw")

        # Filter label~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        label_1 = CTkLabel(self.frame_2_modify, text="Filter habits by category:",
                           font=CTkFont(family="arial", size=16, weight="bold"))
        label_1.grid(column=0, row=0, pady=8, padx=12, sticky="w")

        label_2 = CTkLabel(self.frame_2_modify, text="Your selected habit:",
                           font=CTkFont(family="arial", size=16, weight="bold"))
        label_2.grid(column=1, row=0, pady=8, padx=12, sticky="ew")

        self.selected_habit_label = CTkLabel(self.frame_2_modify, text="None",
                                             font=CTkFont(family="arial", size=25, weight="bold" ), text_color = "#5d4511")
        self.selected_habit_label.grid(column=1, row=2, pady=25, padx=8, sticky="ew", columnspan=2)

        # ~~~~~~~~~~~~~~~~~~~~~~  FUNCTION - Displaying selected habit
        def display_selected_habit_tk(habit):
            self.selected_habit_label.configure(text=habit.name.capitalize())

            undo_today_btn = CTkButton(self.frame_2_modify, text="Undo today's completion",
                                           font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,
                                           height=30, command= lambda: undo_today(habit))
            undo_today_btn.grid(row=8, column=0, padx=15, pady=8, columnspan=2, sticky="nsew")

            undo_date_btn = CTkButton(self.frame_2_modify, text="Undo completion for a date",
                                       font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,
                                       height=30,command = lambda: remove_completion_date(habit))
            undo_date_btn.grid(row=9, column=0, padx=15, pady=8, columnspan=2, sticky="nsew")

            reset_habit_btn = CTkButton(self.frame_2_modify, text="Reset the habit's progress",
                                          font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,height=30,
                                        command= lambda: reset_progress(habit))
            reset_habit_btn.grid(row=10, column=0, padx=15, pady=8, columnspan=2, sticky="nsew")

            rename_habit_btn = CTkButton(self.frame_2_modify, text="Rename the Habit",
                                        font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,
                                        height=30, command=lambda: rename_habit(habit))
            rename_habit_btn.grid(row=11, column=0, padx=15, pady=8, columnspan=2, sticky="nsew")

            change_description_btn = CTkButton(self.frame_2_modify, text="Change habit's description",
                                         font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,
                                         height=30 ,command= lambda: change_description(habit))

            change_description_btn.grid(row=12, column=0, padx=15, pady=8, columnspan=2, sticky="nsew")

            remove_habit_btn = CTkButton(self.frame_2_modify, text="Remove the habit",
                                         font=CTkFont(family="arial", weight="bold", size=14), corner_radius=32,
                                         height=30, command= lambda: remove_habit(habit))
            remove_habit_btn.grid(row=13, column=0, padx=15, pady=8, columnspan=2, sticky="nsew")



        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DROP DOWN HABIT FILTER
        self.filter_and_display_habits_tk("All", self.frame_1_modify, display_selected_habit_tk)
        habit_filter = StringVar(value="All")
        habit_filter_options = CTkOptionMenu(self.frame_2_modify,
                                             variable=habit_filter,
                                             font=CTkFont(family="arial", size=13, weight="bold"),
                                             values=["All", "Daily", "Weekly", "Monthly", "Custom"],
                                             command=lambda i: self.filter_and_display_habits_tk(i, self.frame_1_modify,
                                                                                                 display_selected_habit_tk))

        habit_filter_options.grid(row=2, column=0, pady=10, padx=12, sticky="w")

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MODIFICATION FUNCTIONS
        def undo_today(habit):

            confirmation = CTkMessagebox( title = "Confirmation", message = f"Are you sure you want to undo today's completion for '{habit.name}?'",
                                          icon= "question", option_1= "Yes", option_2 ="No")
            user_chosen= confirmation.get()

            if user_chosen == "No":
                return


            try:
                self.hc.reset_today(habit.name)
                CTkMessagebox(title="Success", message=f"The completion for the habit '{habit.name.capitalize()}' was reset!", icon="check")


            except ValueError as error:
                CTkMessagebox(title="Error", message=str(error), icon="warning")

            self.hc.refresh_habits()

        def reset_progress(habit):

            confirmation = CTkMessagebox(title="Confirmation",
                                         message=f"Are you sure you want to reset the tracking process for '{habit.name}?'",
                                         icon="question", option_1="Yes", option_2="No")
            user_chosen = confirmation.get()

            if user_chosen == "No":
                return

            try:
                self.hc.reset_counter(habit.name)
                CTkMessagebox(title="Success", message=f"The progress for habit  '{habit.name}' was reset", icon="check")
            except ValueError as error:
                CTkMessagebox(title="Error", message=str(error), icon="warning")

            self.hc.refresh_habits()

        #~~~~~~~~~~~~~~~Frame for user prompt
        def rename_habit(habit):
            popup = CTkToplevel(self)
            popup.title("Rename habit")
            popup.geometry("600x300")

            popup.transient(self)



            label = CTkLabel(popup, text= f"Enter the new name for the habit '{habit.name.capitalize()}'",
                             font=CTkFont(family="Arial", size=14, weight="bold"))
            label.pack(pady= 15)


            entry_box = CTkEntry(popup, width=450, font=CTkFont(family="Arial", size=14, weight="bold"))
            entry_box.pack(pady=15)


            def submit_name():

                confirmation = CTkMessagebox(title="Confirmation",
                                             message=f"Are you sure you want to rename the habit '{habit.name}?'",
                                             icon="question", option_1="Yes", option_2="No")
                user_chosen = confirmation.get()

                if user_chosen == "No":
                    return



                new_name = entry_box.get().strip()
                if not new_name:
                    CTkMessagebox(title = "Error", message= "Name cannot be empty", icon = "warning")
                    return

                try:
                    self.hc.rename_habit(habit.name, new_name)
                    CTkMessagebox(title = "Success", message = f"The habit was renamed to {new_name.capitalize()}", icon = "check")


                    popup.destroy()
                    self.modify_habit()

                    #update the selected habit to a new name
                    self.selected_habit_label.configure(text=new_name.capitalize())
                except ValueError as error:
                    CTkMessagebox(title = "Error", message= str(error), icon = "warning")


            submit_button = CTkButton(popup, text="Submit the new name",
                                      font=CTkFont(family="Arial", weight="bold", size=16),
                                      corner_radius=32, height=40, command=submit_name)
            submit_button.pack(pady=15)


        def change_description(habit):
            popup = CTkToplevel(self)
            popup.title("Rename habit")
            popup.geometry("600x300")

            #stays on screen
            popup.transient(self)



            label = CTkLabel(popup, text= f"Enter the new description for the habit - '{habit.name.capitalize()}'",
                             font=CTkFont(family="Arial", size=14, weight="bold"))
            label.pack(pady= 15)


            entry_box = CTkEntry(popup, width=300, height=50, font=CTkFont(family="Arial", size=14, weight="bold"))
            entry_box.pack(pady=15)


            def submit_description():

                confirmation = CTkMessagebox(title="Confirmation",
                                             message=f"Are you sure you want to change the description for '{habit.name}?'",
                                             icon="question", option_1="Yes", option_2="No")
                user_chosen = confirmation.get()

                if user_chosen == "No":
                    return


                new_desc = entry_box.get().strip()
                if not new_desc:
                    CTkMessagebox(title = "Error", message= "Description should not be empty!", icon = "warning")
                    return

                try:
                    self.hc.change_description(habit.name, new_desc)
                    CTkMessagebox(title = "Success", message = f"The description for the habit '{habit.name.capitalize()}' was changed!", icon = "check")


                    popup.destroy()
                    self.modify_habit()



                    #update the selected habit to a new name
                    self.selected_habit_label.configure(text=new_desc.capitalize())

                except ValueError as error:
                    CTkMessagebox(title = "Error", message= str(error), icon = "warning")


            submit_button = CTkButton(popup, text="Change the description",
                                      font=CTkFont(family="Arial", weight="bold", size=16),
                                      corner_radius=32, height=40, command=submit_description)
            submit_button.pack(pady=15)


        def remove_habit(habit):
            confirmation = CTkMessagebox(title="Confirmation",
                                         message=f"Are you sure you want to permanently delete the habit - '{habit.name.capitalize()}?'",
                                         icon="question", option_1="Yes", option_2="No")
            user_chosen = confirmation.get()

            if user_chosen == "No":
                return

            try:
                self.hc.delete_habit(habit.name)
                CTkMessagebox(title="Success",message=f"The habit '{habit.name.capitalize()}' was removed!",icon="check")
                self.modify_habit()

            except ValueError as error:
                CTkMessagebox(title="Error", message=str(error), icon="warning")





        def remove_completion_date(habit):
            popup = CTkToplevel(self)


            popup.title("Remove completion")
            popup.geometry("500x300")
            popup.transient(self)
            calendar_frame = CTkFrame(popup)


            calendar_frame.grid(row=0, column=0, padx=15, pady=15, sticky = "nsew")


            calendar_frame.columnconfigure(0, weight=1)
            calendar_frame.rowconfigure(0, weight=1)
            calendar_frame.rowconfigure(1, weight=1)
            calendar_frame.rowconfigure(2, weight=1)


            header_label = CTkLabel(calendar_frame, width=450, text = "Select the date", font=CTkFont(family="Arial",
                size=14, weight="bold"))
            header_label.grid(row=0, column=0, sticky="ew")

            cal = Calendar(calendar_frame, selectmode="day", year = date.today().year, month = date.today().month, font=("Arial", 20) )

            cal.grid(row= 1,column =0 , sticky = "nsew")

            # colourings for missed days and completed days

            for i in habit.completion_dates:
                cal.calevent_create(i, "Completed", "Completed")

            cal.tag_config("Completed", background="#26C400")

            for i in habit.missed_dates:
                cal.calevent_create(i, "Missed", "Missed")

            cal.tag_config("Missed", background="#C93B1A")



            def confirm_date():
                selected_date = datetime.strptime(cal.get_date(), "%m/%d/%y").date()
                if not selected_date:
                    return

                confirm_notification = CTkMessagebox(title= "Confirm deletion",message = f"Are you sure you want to delete completion for {selected_date.strftime('%d %B %Y')}?",
                                                     icon ="question",option_1 = "Yes", option_2 = "No")

                if confirm_notification.get() == "No":
                    return

                try:
                    self.hc.reset_completion(habit.name, selected_date)
                    CTkMessagebox( title = "Success!", message= "the completion was removed successfully!", icon = "check")
                    popup.destroy()

                    self.modify_habit()

                except ValueError as error:
                    CTkMessagebox( title = "Error", message = str(error), icon = "warning")




            confirm_button = CTkButton(calendar_frame, text="Remove selected completion",
                                       font=CTkFont(family="Arial", size=14, weight="bold"),
                                       corner_radius=32, command=confirm_date)
            confirm_button.grid(row = 4, column = 0, sticky = "ew", pady = 15, padx =10)










#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def habits_statistics(self):
        self.hc.refresh_habits()
        self.clear_screen_tk()
        self.reset_grid()

        self.shown_date = date.today()

        habit_type_filter = StringVar(value="All")
        habit_date_filter = StringVar(value="Lifetime")


        def previous_month():
            month = self.shown_date.month - 1
            year = self.shown_date.year
            if month == 0:
                month = 12
                year -= 1
            self.shown_date = self.shown_date.replace(year=year, month=month)
            update_header()

        def next_month():
            month = self.shown_date.month + 1
            year = self.shown_date.year
            if month == 13:
                month = 1
                year += 1
            self.shown_date = self.shown_date.replace(year=year, month=month)
            update_header()

        def previous_year():
            year = self.shown_date.year - 1
            self.shown_date = self.shown_date.replace(year=year)
            update_header()

        def next_year():
            year = self.shown_date.year + 1
            self.shown_date = self.shown_date.replace(year=year)
            update_header()





        #~~~~~~~~~~~~~~~~~~ month/year header



        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Frames and adjustments
        self.frame_1_statistics = CTkFrame(self.content_display)# left upper screen
        self.frame_1_statistics.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)


        self.frame_2_statistics = CTkFrame(self.content_display)  # the upper right screen
        self.frame_2_statistics.grid(row=1, column=1, columnspan =2, sticky="nsew", padx=15, pady=15)

        self.frame_3_statistics = CTkFrame(self.content_display)  #bottom middle screen
        self.frame_3_statistics.grid(row=2, column=1, sticky="nsew", padx=15, pady=15)

        self.frame_4_statistics = CTkFrame(self.content_display)  # the bottom right screen
        self.frame_4_statistics.grid(row=2, column=2, sticky="nsew", padx=15, pady=15)

        self.frame_5_statistics = CTkFrame(self.content_display) # the left bottom screen
        self.frame_5_statistics.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)



        # columns
        self.content_display.grid_columnconfigure(0, weight=1)
        self.content_display.grid_columnconfigure(1, weight=3)
        self.content_display.grid_columnconfigure(2, weight=3)
        # rows
        self.content_display.grid_rowconfigure(1, weight=1, minsize= 450)
        self.content_display.grid_rowconfigure(0, weight=1)
        self.content_display.grid_rowconfigure(2, weight=1)


        self.frame_1_statistics.grid_columnconfigure(0, weight=1)
        self.frame_1_statistics.grid_columnconfigure(1, weight=1)

        self.frame_4_statistics.grid_columnconfigure(0, weight=1)
        self.frame_4_statistics.grid_columnconfigure(1, weight=1)

        self.frame_2_statistics.grid_columnconfigure(0, weight=1)
        self.frame_2_statistics.grid_rowconfigure(0, weight=1)



        self.frame_2_statistics.grid_columnconfigure(1, weight=1)


        # month names ruins the structure
        self.frame_1_statistics.grid_columnconfigure(1, minsize=210)



        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Labels
        title = CTkLabel(self.content_display, text="Habit Statistics", font=CTkFont(family="arial", weight="bold", size=25))
        title.grid(row=0, column=0, pady=7, padx=25 , sticky = "w")


        filter_type_label = CTkLabel(self.frame_1_statistics, text="Filter by type:",
                                     font=CTkFont(family="arial", weight="bold", size=15))
        filter_type_label.grid(row=0, column=0, pady=3, padx=10, sticky = "w")

        filter_date_label = CTkLabel(self.frame_1_statistics, text="Filter by date:",
                                     font=CTkFont(family="arial", weight="bold", size=15))
        filter_date_label.grid(row=0, column=1, pady=3, padx=10)


        overview_label = CTkLabel(self.frame_1_statistics, text ="Overall Statistics:",
                            font = CTkFont(family="arial", weight="bold", size=20), text_color="#5d4511")

        overview_label.grid(row =4 , column= 0, pady =3, padx =15, columnspan = 2, sticky = "w")



        #~~~~~~~~~~~~~~~~~~~ Overview progress labels



        total_habits_label = CTkLabel(self.frame_1_statistics, text="Total Habits:",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="#5d4511")

        completions_label = CTkLabel(self.frame_1_statistics, text="Total Completions:",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="#5d4511")
        missed_label= CTkLabel(self.frame_1_statistics, text="Total Missed:",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="#5d4511")

        consistency_label = CTkLabel(self.frame_1_statistics, text="Consistency %",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="#5d4511")





        total_habits_label.grid(row =6 , column= 0, pady =5, padx =12, sticky ="w")

        completions_label.grid(row =7 , column= 0, pady =5, padx =12, sticky ="w")

        missed_label.grid(row =8 , column= 0, pady =5, padx =12, sticky ="w")

        consistency_label.grid(row =9 , column= 0, pady =5, padx =12, sticky ="w")


        #~~~~~~~~~~~~~~~~~~~~~~~~dynamic labels




        total_habits_2_label = CTkLabel(self.frame_1_statistics, text=f"",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="black")

        total_completions_2_label =CTkLabel(self.frame_1_statistics, text=f"",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="black")

        missed_2_label = CTkLabel(self.frame_1_statistics, text=f"",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="black")

        consistency_2_label= CTkLabel(self.frame_1_statistics, text=f"",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color="black")


        total_habits_2_label.grid(row=6, column=1, pady=5, padx=12)

        total_completions_2_label.grid(row=7, column=1, pady=5, padx=12)

        missed_2_label.grid(row=8, column=1, pady=5, padx=12)

        consistency_2_label.grid(row=9, column=1, pady=5, padx=12)




        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DROP DOWN MENU


        habit_type_options = CTkOptionMenu(self.frame_1_statistics,
                                             variable=habit_type_filter,
                                             font=CTkFont(family="arial", size=13, weight="bold"),
                                             values=["All", "Daily", "Weekly", "Monthly", "Custom"],
                                           command = lambda _: update_header())
        habit_type_options.grid(row= 1, column =0, sticky = "w", pady = 8, padx= 10)




        habit_date_options = CTkOptionMenu(self.frame_1_statistics,
                                             variable=habit_date_filter,
                                             font=CTkFont(family="arial", size=13, weight="bold"),
                                             values=["Lifetime" ,"Yearly", "Monthly"],
                                           command= lambda _: update_header())
        habit_date_options.grid(row=1, column=1, pady=8, padx=10)





        date_header = CTkLabel(self.frame_1_statistics, text= "All",
                          font=CTkFont(family="arial", size=18, weight="bold") )

        date_header.grid(row= 2, column = 0, columnspan=2, pady =5, padx= 10, sticky = "ew")


        buttons_frame = CTkFrame(self.frame_1_statistics, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=3)

        spacer = CTkLabel(buttons_frame, text="",height=37)
        spacer.grid(row=0, column=0)



        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)


        # Worst and best habits:

        worst_name, worst_score = self.hc.worst_habit()
        best_name, best_score = self.hc.best_habit()


        #current best streak

        current_best_habit, current_best_streak = self.hc.current_best_streak()




        title_best_worst_label = CTkLabel(self.frame_5_statistics, text="Your top and worst habit scores:",
                                  font=CTkFont(family="arial", weight="bold", size=18), text_color="#5d4511")

        worst_habit_label = CTkLabel(self.frame_5_statistics, text="Worst habit:",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color= "#A72626")

        best_habit_label = CTkLabel(self.frame_5_statistics, text="Best Habit:",
                                  font=CTkFont(family="arial", weight="bold", size=14), text_color ="#27522B")



        worst_result_label = CTkLabel(self.frame_5_statistics, text=f"{worst_name.capitalize()}: {round(worst_score,1)}%",
                                  font=CTkFont(family="arial", weight="bold", size=14))

        best_result_label= CTkLabel(self.frame_5_statistics, text=f"{best_name.capitalize()}: {round(best_score,1)}%",
                                  font=CTkFont(family="arial", weight="bold", size=14))

        best_streak_label = CTkLabel(self.frame_5_statistics, text="Current best streak:",
                                  font=CTkFont(family="arial", weight="bold", size=15), text_color="#5d4511")

        best_streak_result_label = CTkLabel(self.frame_5_statistics, text= f"{current_best_habit}:     {current_best_streak} ",
                                  font=CTkFont(family="arial", weight="bold", size=14))

        title_best_worst_label.grid(row=0, column=0, pady=5, columnspan= 2, padx=12, sticky="e")



        best_habit_label.grid(row=2, column=0, pady=5, padx=12, sticky="w")

        best_result_label.grid(row=2, column=1, pady=5, padx=12, sticky="w")

        worst_habit_label.grid(row=3, column=0, pady=5, padx=12, sticky="w")

        worst_result_label.grid(row=3, column=1, pady=5, padx=12,  sticky="w")



        best_streak_label.grid(row=5, column=0, columnspan =2, pady=6, padx=12, sticky="w")

        best_streak_result_label.grid(row=6, column=0, pady=5,columnspan =2, padx=12, sticky = "w")



        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Progress Bar
        progress_label = CTkLabel(self.frame_4_statistics, text="Progress bar:",
                                  font=CTkFont(family="arial", weight="bold", size=18))


        progress_picture = CTkProgressBar(self.frame_4_statistics, height = 40)

        progress_percent_label = CTkLabel(self.frame_4_statistics, text=" / 100 ",
                                font=CTkFont(family="arial", weight="bold", size=15), text_color="#5d4511")


        #normalizing for the progress bar
        progress_value = self.hc.goal_percentage() / 100
        progress_picture.set(progress_value)

        progress_percent_label.configure(text = f"{round(self.hc.goal_percentage(),1)}% / 100%")


        #fixing the graph in place
        self.frame_3_statistics.grid_rowconfigure(0, weight=1, minsize=300)
        self.frame_3_statistics.grid_columnconfigure(0, weight=1, minsize= 300)



        progress_label.grid(row=0, column=0, sticky="ew", padx=12, pady=20, columnspan=2)


        progress_picture.grid(row=2, column=0, padx=8, pady=8, sticky="ew", columnspan=2)

        progress_percent_label.grid(row=3, column=0, columnspan=2, sticky="ew", padx=12, pady=8)



        def update_header():
            for w in self.frame_3_statistics.winfo_children():
                w.destroy()

            date_format = habit_date_filter.get()


            if date_format == "Yearly":
                date_header.configure( text= f"Year {self.shown_date.strftime('%Y')}",
                          font=CTkFont(family="arial", size=18, weight="bold"))
            elif date_format == "Monthly":
                date_header.configure( text=self.shown_date.strftime("%B %Y"),
                          font=CTkFont(family="arial", size=18, weight="bold"))
            else:
                date_header.configure( text= "All",
                          font=CTkFont(family="arial", size=18, weight="bold"))

            for widget in buttons_frame.winfo_children():
                widget.destroy()


            if date_format == "Monthly":

                next_month_btn = CTkButton(buttons_frame, text="◀", width=40, command=previous_month)
                next_month_btn.grid(row=0, column = 0, pady= 5, padx= 10, sticky = "w")

                next_month_btn =  CTkButton(buttons_frame, text="▶", width=40, command=next_month)
                next_month_btn.grid(row=0, column=1, pady=5, padx=10, sticky="w")


            elif date_format == "Yearly":
                prev_year_btn = CTkButton(buttons_frame, text="◀", width=40, command=previous_year)
                prev_year_btn.grid(row=0, column = 0, pady= 5, padx= 10, sticky = "w")

                next_year_btn = CTkButton(buttons_frame, text="▶", width=40, command=next_year)
                next_year_btn.grid(row=0, column=1, pady=5, padx=10, sticky="e")

            else:
                non_btn = CTkButton(buttons_frame, text="◀", width=40)
                non_btn.grid(row=0, column=0, pady=5, padx=10, sticky="w")

                non2_btn = CTkButton(buttons_frame, text="▶", width=40)
                non2_btn.grid(row=0, column=1, pady=5, padx=10, sticky="e")


            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Pie Chart


            #obtain total completions and total missed dates

            # I do not know why, but I have tried to call the filter_habits function in the graph file
            # And it just didn't work, even if the functions had same inputs. No clue why, wasted 4 hours here


            missed, completed, total_consistency = self.hc.totals_sorted(date_format, habit_type_filter.get(),self.shown_date)



            #configure the labels:
            total_completions_2_label.configure( text = f"{completed}")
            missed_2_label.configure(text =f"{missed}")
            consistency_2_label.configure(text = f"{total_consistency}%")



            sorted_habits, completed_dates, missed_dates_fn = self.hc.filter_habits(date_format, habit_type_filter.get(),self.shown_date)


            self.gr.draw_consistency_pie(self.frame_3_statistics,completed=completed,missed=missed)

            self.gr.line_chart(self.frame_2_statistics, completed_dates, date_format, self.shown_date)



            # Updating the habit
        update_header()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Analyse habit

    def analyse_habit(self):

        self.hc.refresh_habits()

        self.clear_screen_tk()
        self.reset_grid()

        self.shown_date = date.today()


        # ~~~~~~~~~~~~~~~~~~Frames

        self.analyse_frame_1 = CTkScrollableFrame(self.content_display, label_text="Select a habit",  # the left screen
                                               label_font=CTkFont(family="arial", size=17, weight="bold"))
        self.analyse_frame_1.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        self.analyse_frame_2 = CTkFrame(self.content_display)  # the right screen
        self.analyse_frame_2.grid(row=1, column=1, sticky="nsew", padx=15, pady=10)





        # columns
        self.content_display.grid_columnconfigure(0, weight=0)
        self.content_display.grid_columnconfigure(1, weight=1)
        # rows
        self.content_display.grid_rowconfigure(1, weight=1)
        self.content_display.grid_rowconfigure(0, weight=0)

        #adjusting the frame weight
        self.analyse_frame_2.grid_columnconfigure(0, weight =1)
        self.analyse_frame_2.grid_columnconfigure(1, weight=1)
        self.analyse_frame_2.grid_columnconfigure(2, weight=1)




        # Labels
        title = CTkLabel(self.content_display, text="Analyse Habit",
                         font=CTkFont(family="arial", size=25, weight="bold"))
        title.grid(column=0, row=0, pady=10, padx=10, sticky="nw")

        # Filter label~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        label_1 = CTkLabel(self.analyse_frame_2, text="Filter habits by category:",
                           font=CTkFont(family="arial", size=16, weight="bold"))
        label_1.grid(column=0, row=0, pady=8, padx=10, sticky="w")

        label_2 = CTkLabel(self.analyse_frame_2, text="Your selected habit:",
                           font=CTkFont(family="arial", size=16, weight="bold"))
        label_2.grid(column=1, row=0, pady=8, padx=10)

        self.selected_habit_label = CTkLabel(self.analyse_frame_2, text="None",
                                             font=CTkFont(family="arial", size=18, weight="bold"), text_color="#5d4511")
        self.selected_habit_label.grid(column=1, row=1, pady=20, padx=8, sticky="ew", columnspan=2)



        def display_selected_habit_tk(habit):
            self.selected_habit_label.configure(text=habit.name.capitalize())
            habit_calendar(habit)

            # destroy other widgets, otherwise it ruins the design
            for widget in self.analyse_frame_2.grid_slaves():
                if int(widget.grid_info()["row"]) >= 7:
                    widget.destroy()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ HABIT INFO LABELS

            main_label = CTkLabel(self.analyse_frame_2, text="Overview:",
                           font=CTkFont(family="arial", size=18, weight="bold"))

            completions_label=CTkLabel(self.analyse_frame_2, text=f"Total Completions:   {habit.completed_reps}",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")


            missed_label =CTkLabel(self.analyse_frame_2, text=f"Missed Completions:   {habit.completions_missed}",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")


            best_streak_label = CTkLabel(self.analyse_frame_2, text=f"Best Streak:   {habit.best_streak}",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")


            current_streak_label=CTkLabel(self.analyse_frame_2, text=f"Current Streak:   {habit.current_streak}",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")




            approximate_label=CTkLabel(self.analyse_frame_2, text=f"Approximate Completion Date:  {habit.approximate_completion}",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")

            goal_label = CTkLabel(self.analyse_frame_2, text=f"Goal:  {habit.completed_reps} / {habit.goal_count}",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")

            creation_date_label = CTkLabel(self.analyse_frame_2, text=f"Creation date:  {habit.creation_date}",
                                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")


            deadline_label = CTkLabel(self.analyse_frame_2, text=f"Next Completion Deadline:  {habit.next_deadline}",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")



            habit_score_label= CTkLabel(self.analyse_frame_2, text=f"Performance Score:   {round(habit.performance_score,1)}%",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")



            consistency_label =CTkLabel(self.analyse_frame_2, text=f"Consistency:   {round(habit.consistency_ratio,1)}%",
                           font=CTkFont(family="arial", size=15, weight="bold"), text_color="#5d4511")




            main_label.grid(row=7, column=0, padx=15, pady=15, sticky="w")

            completions_label.grid(row=8, column=0, padx=15, pady=7, sticky="w")

            missed_label.grid(row=9, column=0, padx=15, pady=7, sticky="w")

            current_streak_label.grid(row=10, column=0, padx=15, pady=7, sticky="w")

            consistency_label.grid(row=11, column=0, padx=15, pady=7, sticky="w")

            habit_score_label.grid(row=8, column=1, padx=15, pady=7, sticky="w")

            best_streak_label.grid(row=9, column=1, padx=15, pady=7, sticky="w")

            deadline_label.grid(row=10, column=1, padx=15, pady=7, sticky="w")

            approximate_label.grid(row=11, column=1, padx=15, pady=10, sticky="w")

            creation_date_label.grid(row =12, column =0,padx=15, pady=10, sticky="w")

            goal_label.grid(row =12, column =1,padx=15, pady=10, sticky="w")

            def description(habit):
                popup = CTkToplevel(self)
                popup.title("Habit description")
                popup.geometry("700x400")

                popup.transient(self)
                instruction_text = habit.description

                instruction_text_box = CTkTextbox(popup, width=500, height=300,
                                                  font=CTkFont(family="Arial", size=14, weight="bold"))
                instruction_text_box.insert("0.0", instruction_text)
                instruction_text_box.configure(state="disabled")
                instruction_text_box.pack()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Description Button

            desc_btn = CTkButton(self.analyse_frame_2, text="Habit Description",
                                 font=CTkFont(family="Arial", size=14, weight="bold"),
                                 corner_radius=32, command=lambda: description(habit))

            desc_btn.grid(row=7, column=1, sticky="w")




        #~~~~~~~~~~~~~~~~~~~ DROP DOWN MENU
        self.filter_and_display_habits_tk("All", self.analyse_frame_1, display_selected_habit_tk)
        habit_filter = StringVar(value="All")
        habit_filter_options = CTkOptionMenu(self.analyse_frame_2,
                                             variable=habit_filter,
                                             font=CTkFont(family="arial", size=13, weight="bold"),
                                             values=["All", "Daily", "Weekly", "Monthly", "Custom"],
                                             command=lambda i: self.filter_and_display_habits_tk(i, self.analyse_frame_1,
                                                                                                 display_selected_habit_tk))

        habit_filter_options.grid(row=1, column=0, pady=10, padx=15, sticky="w")



        def habit_calendar(habit):

            #where was this module, when I needed it :(

            if hasattr(self, "habit_calendar"):
                self.habit_calendar.destroy()


            calander_title = CTkLabel(self.analyse_frame_2, text="Completion Calendar",
                           font=CTkFont(family="arial", size=20, weight="bold"))

            calander_title.grid(row = 2 , column = 0, columnspan = 2, sticky = "ew")



            self.habit_calendar = Calendar(self.analyse_frame_2, selectmode= "none", year = self.shown_date.year ,
                                           font=("Arial", 11),month = self.shown_date.month )

            self.habit_calendar.grid(row = 3, column = 0, columnspan = 2, rowspan =4, padx = 15, pady = 15, sticky= "nsew")


            # colourings for missed days and completed days

            for i in habit.completion_dates:
                self.habit_calendar.calevent_create(i,"Completed", "Completed")

            self.habit_calendar.tag_config("Completed", background = "#26C400")

            for i in habit.missed_dates:
                self.habit_calendar.calevent_create(i,"Missed", "Missed")

            self.habit_calendar.tag_config("Missed", background="#C93B1A")

    #~~~~~~~~~~~~~~~ Save and exit~~~~~~~~~~~~

    def save_and_exit(self):
        #close the sql connection
        self.hc.exit_application()

        self.quit()
        self.destroy()





if __name__ == "__main__":
    app = App()
    app.mainloop()
    hc = HabitControl()
    hc.load_habits()
