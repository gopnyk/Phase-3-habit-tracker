from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTkLabel, CTkFont
import calendar
from Habits import HabitControl
from DB1 import DBHandler
from tkinter import BOTH
from matplotlib.ticker import MaxNLocator


class Graphs:
    def __init__(self):
        self.canvas = None
        dh = DBHandler("DB1.db")
        self.hc = HabitControl(dh)

    def clear(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def draw_consistency_pie(self, parent_frame, completed, missed):
        # Clear existing widgets in parent frame
        for w in parent_frame.winfo_children():
            w.destroy()


        # locks the frame size, so the graph does not explode in size
        parent_frame.grid_rowconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(0, weight=1)


        if completed + missed == 0:
            CTkLabel(
                parent_frame,
                text="No data available",
                font=CTkFont(size=16, weight="bold")
            ).grid(row=0, column=0, padx=10, pady=10)
            return

        fig = Figure(figsize=(0.1, 0.1), facecolor= "#b19174")
        ax = fig.add_subplot(111)

        ax.pie([completed, missed],labels=["Completed", "Missed"],autopct="%1.1f%%",startangle=80,radius=0.70,
               colors= ["#8aae30", "#c84738"])

        ax.set_title("Consistency")
        ax.set_aspect("equal")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,sticky="nsew")




    def line_chart(self, parent_frame, completion_dates, time_filter, selected_day):


        for w in parent_frame.winfo_children():
            w.destroy()



        # First x values must be adjusted. we want the months/days to appear as integer number.
        # check if the completion date matches users selected date filter by month and year.
        # if it checks out add it to the x_dates. x refers to the integer month values
        cal = calendar.Calendar()
        x_dates = []
        x = []
        y = []


        #itermonthdates returns the dates of the selected month. (in generator form)
        # we convert them to date format and check against the actual completion dates.
        # if they match - y gets the date as key and completion count

        if time_filter == "Monthly":
            for i in cal.itermonthdates(selected_day.year, selected_day.month):
                if i.month == selected_day.month:
                    x_dates.append(i)
                    x.append(i.day)

            y = [completion_dates.get(i, 0) for i in x_dates]

        # x will display integers from 1 to 12 - each represents month
        # counts the total completions for each month, and checks if it matches user's selected year (for m in x)

        elif time_filter == "Yearly":
            x = list(range(1, 13))
            y = [sum(completion_count for i, completion_count in completion_dates.items()
                     if i.month == month and i.year == selected_day.year) for month in x]

        # For lifetime, x variables will be the years with total completions
        #first it extracts the years from completed dates.
        # then it sums all the completed filtered by the year
        elif time_filter == "Lifetime":
            years = sorted({d.year for d in completion_dates})
            x = years
            y = [sum(cnt for d, cnt in completion_dates.items() if d.year == yr) for yr in years]




        # No data guard - simple label
        if not y or all(v == 0 for v in y):
            CTkLabel(parent_frame, text="No data available",
                     font=CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky ="nsew")
            return

        # Draw chart
        fig = Figure(figsize=(2, 1), facecolor="#b19174")

        ax = fig.add_subplot(111)

        # graph configurations
        ax.grid(True, alpha=0.3)
        ax.plot(x, y, marker='o', color = "#cecccc" )
        ax.set_facecolor("#705842")
        fig.tight_layout(pad=0.5)
        ax.set_xlabel("Date")
        ax.set_ylabel("Completions")
        ax.set_title("Habit Completions Over Time")


        #adjusting the x-axis values~~~~~~~~~~~~

        if time_filter == "Monthly":
            #every two days
            ax.set_xticks(x[::2])
            ax.tick_params(axis='x')

        elif time_filter == "Yearly":
            month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            ax.set_xticks(x)
            ax.set_xticklabels(month_labels, fontsize=8)
            ax.set_xlim(1, 12)

        elif time_filter == "Lifetime":
            ax.set_xticks(x)
            ax.set_xticklabels([str(year) for year in x], fontsize=8)

        #adjusting the y-axis values to integers

        ax.yaxis.set_major_locator(MaxNLocator(integer=True))



        # displaying the graph in the selected frame (statistics)
        self.canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = BOTH ,expand = True)














