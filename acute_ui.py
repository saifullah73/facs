import tkinter as tk
from tkinter import StringVar, IntVar
from tkinter import ttk

from ttkthemes import ThemedTk


class AcuteUI:
    def __init__(self):
        self.window = self.generate_main_window()
        self.selected_city_var = StringVar()
        self.selected_scenario_var = StringVar()
        self.start_infect_int_var = IntVar()
        self.start_infect_str_var = StringVar()
        self.sim_len_str_var = StringVar()
        self.transition_day_var = StringVar()
        self.case_multiplier_var = StringVar()
        self.sim_len_int_var = IntVar()
        self.window = self.draw_title_frame()
        self.window, self.run_btn, self.output = self.draw_options_frame()

    def enable_run_button(self, enable):
        if enable:
            self.run_btn.configure(state=tk.NORMAL)
        else:
            self.run_btn.configure(state=tk.DISABLED)

    def generate_main_window(self):
        self.window = ThemedTk(theme="arc")
        w = 700
        h = 430  # original 450
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.window.resizable(0, 0)
        self.window.title("ACUTE Simulation Framework")
        self.window.iconbitmap("icon.ico")
        self.window.configure(bg='white')
        return self.window

    def draw_title_frame(self):
        s = ttk.Style()
        s.configure('My.TFrame', background='white')
        self.upper_frame = ttk.Frame(self.window, width=800, height=50, style='My.TFrame')
        self.upper_frame.grid(row=0, column=0)
        self.title_label = ttk.Label(self.upper_frame, text="Configure your Simulation", font=('Arial', 22),
                                     background='white',
                                     foreground="#5293e2")
        self.title_label.place(x=340, y=25, anchor="center")
        return self.window

    def start_infect_scale_callback(self, value):
        self.start_infect_entry.delete(0, "end")
        self.start_infect_entry.insert(0, str(int(float(value))))

    def sim_len_scale_callback(self, value):
        self.sim_len_entry.delete(0, "end")
        self.sim_len_entry.insert(0, str(int(float(value))))

    def start_infect_entry_callback(self):
        try:
            i = int(self.start_infect_str_var.get())
            if 10 <= i <= 1000:
                self.start_infect_scale.set(i)
            else:
                self.start_infect_entry.delete(0, "end")
                self.start_infect_entry.insert(0, str(self.start_infect_int_var.get()))
        except ValueError:
            self.start_infect_entry.delete(0, "end")
            self.start_infect_entry.insert(0, str(self.start_infect_int_var.get()))
        return True

    def sim_len_entry_callback(self):
        try:
            i = int(self.sim_len_str_var.get())
            if 30 <= i <= 365:
                self.sim_len_scale.set(i)
            else:
                self.sim_len_entry.delete(0, "end")
                self.sim_len_entry.insert(0, str(self.sim_len_int_var.get()))
        except ValueError:
            self.sim_len_entry.delete(0, "end")
            self.sim_len_entry.insert(0, str(self.sim_len_int_var.get()))
        return True

    def transition_day_entry_callback(self):
        if self.transition_day_var.get() != "":
            try:
                i = int(self.transition_day_var.get())
                sl = int(self.sim_len_str_var.get())
                if i <= sl:
                    self.transition_day_entry.delete(0, "end")
                    self.transition_day_entry.insert(0, str(i))
                    self.transition_day_info_label.config(foreground="grey")
                else:
                    self.transition_day_entry.delete(0, "end")
                    self.transition_day_entry.insert(0, str(i))
                    self.transition_day_info_label.config(foreground="red")
            except ValueError:
                self.transition_day_entry.delete(0, "end")
                self.transition_day_info_label.config(foreground="red")
                self.transition_day_var.set("30")
        else:
            self.transition_day_var.set("30")
        return True

    def case_multiplier_entry_callback(self):
        if self.case_multiplier_var.get() != "":
            try:
                i = float(self.case_multiplier_var.get())
                if 0.0 <= i <= 1.0:
                    self.case_multiplier_entry.delete(0, "end")
                    self.case_multiplier_entry.insert(0, str(i))
                    self.case_isolation_info_label.config(foreground="grey")
                else:
                    self.case_multiplier_entry.delete(0, "end")
                    self.case_multiplier_entry.insert(0, str(i))
                    self.case_isolation_info_label.config(foreground="red")
            except ValueError:
                self.case_multiplier_entry.delete(0, "end")
                self.case_isolation_info_label.config(foreground="red")
                self.case_multiplier_var.set("0.625")
        else:
            self.case_multiplier_var.set("0.625")
        return True

    def make_command(self, widget):
        widget.master.focus_set()
        self.start_infect_entry_callback()
        self.sim_len_entry_callback()
        self.transition_day_entry_callback()
        self.case_multiplier_entry_callback()
        print(
            f"python run.py --location={self.selected_city_var.get()} --transition_scenario={self.selected_scenario_var.get()} --transition_day={self.transition_day_var.get()} "
            f"--ci_multiplier={self.case_multiplier_var.get()} --starting_infections={self.start_infect_int_var.get()} --sim_length={self.sim_len_int_var.get()}")
        return self.selected_city_var.get(), self.selected_scenario_var.get(), self.transition_day_var.get(), self.case_multiplier_var.get(), self.start_infect_int_var.get(), self.sim_len_int_var.get()

    def combo_box_callback(self, event):
        event.widget.selection_clear()
        event.widget.master.focus_set()

    def draw_options_frame(self):
        s = ttk.Style()
        s.configure('My.TFrame', background='white')
        s.configure('My.TRadiobutton', background='white')
        s.configure("My.Horizontal.TScale", background="white")
        self.bottom_frame = ttk.Frame(self.window, width=800, height=410, style='My.TFrame')
        self.bottom_frame.grid(row=1, column=0)

        self.city_label = ttk.Label(self.bottom_frame, text="Choose City:", font=('Calibri', 12), background='white',
                                    foreground="grey")
        self.city_label.place(x=101.5, y=15, anchor="center")

        self.selected_city_var.set("Islamabad")
        self.city = ttk.Combobox(self.bottom_frame, textvariable=self.selected_city_var, state="readonly",
                                 takefocus=False,
                                 values=[
                                     "Islamabad", "Abbottabad"])
        self.city.place(x=460, y=15, width=350, anchor="center")
        self.city.current(0)
        self.city.bind("<<ComboboxSelected>>", self.combo_box_callback)

        self.scenario_label = ttk.Label(self.bottom_frame, text="Choose Transition Scenario:", font=('Calibri', 12),
                                        background='white', foreground="grey")
        self.scenario_label.place(x=61, y=40)

        self.selected_scenario_var.set("extend-lockdown")

        self.no_measure_rb = ttk.Radiobutton(self.bottom_frame, text="No measures", variable=self.selected_scenario_var,
                                             value="no-measures",
                                             style='My.TRadiobutton',
                                             takefocus=False)
        self.no_measure_rb.place(x=282, y=40)

        self.extend_rb = ttk.Radiobutton(self.bottom_frame, text="Extend lockdown", variable=self.selected_scenario_var,
                                         value="extend-lockdown", style='My.TRadiobutton',
                                         takefocus=False)
        self.extend_rb.place(x=505, y=40)

        self.dynamic_rb = ttk.Radiobutton(self.bottom_frame, text="Dynamic Lockdown",
                                          variable=self.selected_scenario_var,
                                          value="dynamic-lockdown", style='My.TRadiobutton',
                                          takefocus=False)
        self.dynamic_rb.place(x=282, y=65)

        self.periodic_rb = ttk.Radiobutton(self.bottom_frame, text="Periodic Lockdown",
                                           variable=self.selected_scenario_var,
                                           value="periodic-lockdown", style='My.TRadiobutton',
                                           takefocus=False)
        self.periodic_rb.place(x=505, y=65)

        self.smart_rb = ttk.Radiobutton(self.bottom_frame, text="Smart Lockdown", variable=self.selected_scenario_var,
                                        value="smart-lockdown", style='My.TRadiobutton',
                                        takefocus=False)
        self.smart_rb.place(x=282, y=90)

        self.work_50_rb = ttk.Radiobutton(self.bottom_frame, text="Work 50%", variable=self.selected_scenario_var,
                                          value="work50",
                                          style='My.TRadiobutton', takefocus=False)
        self.work_50_rb.place(x=505, y=90)

        self.work_75_rb = ttk.Radiobutton(self.bottom_frame, text="Work 75%", variable=self.selected_scenario_var,
                                          value="work75",
                                          style='My.TRadiobutton', takefocus=False)
        self.work_75_rb.place(x=282, y=115)

        self.work_100_rb = ttk.Radiobutton(self.bottom_frame, text="Work 100%", variable=self.selected_scenario_var,
                                           value="work100",
                                           style='My.TRadiobutton',
                                           takefocus=False)
        self.work_100_rb.place(x=505, y=115)

        self.transition_day_label = ttk.Label(self.bottom_frame, text="Transition Day:", font=('Calibri', 12),
                                              background='white',
                                              foreground="grey")
        self.transition_day_label.place(x=61, y=150)

        self.transition_day_var.set("30")
        self.transition_day_entry = ttk.Entry(self.bottom_frame, font=('Calibri', 12),
                                              textvariable=self.transition_day_var,
                                              validate="focusout",
                                              validatecommand=self.transition_day_entry_callback)
        self.transition_day_entry.place(x=285, y=150, width=350)

        self.transition_day_info_label = ttk.Label(self.bottom_frame,
                                                   text="*Integer value, Must be less than Simulation length value, default= 30",
                                                   font=('Calibri', 8), background='white',
                                                   foreground="grey")
        self.transition_day_info_label.place(x=285, y=180)

        self.case_multiplier_label = ttk.Label(self.bottom_frame, text="Case Isolation Multiplier:",
                                               font=('Calibri', 12),
                                               background='white', foreground="grey")
        self.case_multiplier_label.place(x=61, y=200)

        self.case_multiplier_var.set("0.625")
        self.case_multiplier_entry = ttk.Entry(self.bottom_frame, font=('Calibri', 12),
                                               textvariable=self.case_multiplier_var,
                                               validate="focusout",
                                               validatecommand=self.case_multiplier_entry_callback)
        self.case_multiplier_entry.place(x=285, y=200, width=350)

        self.case_isolation_info_label = ttk.Label(self.bottom_frame,
                                                   text="*Float value between 0 and 1, default= 0.625",
                                                   font=('Calibri', 8), background='white',
                                                   foreground="grey")
        self.case_isolation_info_label.place(x=285, y=230)

        self.start_infect_label = ttk.Label(self.bottom_frame, text="Starting Infections:", font=('Calibri', 12),
                                            background='white',
                                            foreground="grey")
        self.start_infect_label.place(x=61, y=250)

        self.start_infect_int_var.set(500)

        self.start_infect_scale = ttk.Scale(self.bottom_frame, from_=10, to=1000, variable=self.start_infect_int_var,
                                            command=self.start_infect_scale_callback,
                                            style="My.Horizontal.TScale", value=500)
        self.start_infect_scale.place(x=285, y=257, width=295)

        self.start_infect_str_var.set(500)

        self.start_infect_entry = ttk.Entry(self.bottom_frame, font=('Calibri', 12),
                                            textvariable=self.start_infect_str_var,
                                            validate="focusout", validatecommand=self.start_infect_entry_callback)
        self.start_infect_entry.place(x=585, y=250, width=50)

        self.sim_len_label = ttk.Label(self.bottom_frame, text="Simulation Length:", font=('Calibri', 12),
                                       background='white',
                                       foreground="grey")
        self.sim_len_label.place(x=61, y=285)

        self.sim_len_int_var.set(365)

        self.sim_len_scale = ttk.Scale(self.bottom_frame, from_=30, to=365, variable=self.sim_len_int_var,
                                       command=self.sim_len_scale_callback,
                                       style="My.Horizontal.TScale", value=365)
        self.sim_len_scale.place(x=285, y=292, width=295)

        self.sim_len_str_var.set(365)
        self.sim_len_entry = ttk.Entry(self.bottom_frame, font=('Calibri', 12), textvariable=self.sim_len_str_var,
                                       validate="focusout",
                                       validatecommand=self.sim_len_entry_callback)
        self.sim_len_entry.place(x=585, y=285, width=50)

        self.run_sim_button = ttk.Button(self.bottom_frame, text="Run Simulation",
                                         # command=lambda: self.make_command(self.run_sim_button),
                                         takefocus=False)
        self.run_sim_button.place(x=250, y=330, width=200)

        self.output_label = ttk.Label(self.bottom_frame, text="", font=('Calibri', 12),
                                      background='white', foreground="green", anchor="center")
        self.output_label.place(x=61, y=370, width=580)

        return self.window, self.run_sim_button, self.output_label


if __name__ == "__main__":
    ui = UI()

    # ui.window.mainloop()
