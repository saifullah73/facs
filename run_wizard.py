import queue as qq
import threading
import time
import acute_ui as au
import run_sim as rs


class GuiPart:
    def __init__(self, master, outputLabel, queue, endCommand):
        self.queue = queue
        self.outputLabel = outputLabel
        master.window.protocol("WM_DELETE_WINDOW", endCommand)

    def process_incoming_msg(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.outputLabel.config(text=msg)
            except qq.Empty:
                pass


class ThreadedClient:
    def __init__(self, master):
        self.running = 0
        self.master = master
        self.sim_thread = None
        self.queue = qq.Queue()
        self.gui = GuiPart(master, master.output, self.queue, self.endApplication)
        self.master.run_btn.configure(command=self.run_btn_callback)

    def run_btn_callback(self):
        self.running = 1
        self.sim_thread = threading.Thread(target=self.start_simulation)
        self.sim_thread.start()
        self.periodic_callback()

    def periodic_callback(self):
        self.gui.process_incoming_msg()
        if self.running:
            self.master.window.after(200, self.periodic_callback)

    def start_simulation(self):
        while self.running:
            a, b, c, d, e, f = self.master.make_command(self.master.run_btn)
            if int(c) <= int(f):
                if 0.0 <= float(d) <= 1.0:
                    self.master.enable_run_button(enable=False)
                    self.master.transition_day_info_label.config(foreground="grey")
                    self.master.case_isolation_info_label.config(foreground="grey")
                    self.master.window.geometry("700x460")
                    rs.run_simulation(queue=self.queue, location=a, running=self.running, transition_scenario=b,
                                      ci_multiplier=d,
                                      starting_infections=e, transition_day=c, sim_length=f)
                    self.master.enable_run_button(enable=True)
                    self.endSimulation()
                else:
                    self.master.case_isolation_info_label.config(foreground="red")
                    self.endSimulation()
            else:
                self.master.transition_day_info_label.config(foreground="red")
                self.endSimulation()

    def endApplication(self):
        self.running = 0
        self.master.window.destroy()

    def endSimulation(self):
        self.running = 0


if __name__ == "__main__":
    ui = au.AcuteUI()
    client = ThreadedClient(ui)
    ui.window.mainloop()
