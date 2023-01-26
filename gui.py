import tkinter as tk
from capture_pic import CapturePic
from load_project import LoadProject
import datetime
from PIL import Image, ImageTk
import configparser


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        # Initialize Window
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        pages = (
            LoadExistingProject,
            StartPage,
            CreateNewProject,
            CapturePicInterface
        )
        # Load all pages
        for F in pages:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    # shows the desired frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Capture Pic")
        label.pack(pady=10, padx=10)

        button = tk.Button(
            self,
            text="Create New Experiment",
            command=lambda: controller.show_frame(CreateNewProject))
        button.pack()

        load_existing_project = self.controller.get_page(LoadExistingProject)
        if len(load_existing_project.OPTIONS) > 0:
            load_button_state = 'normal'
        else:
            load_button_state = 'disabled'

        button2 = tk.Button(
            self,
            text="Load Existing Experient",
            state=load_button_state,
            command=lambda: controller.show_frame(LoadExistingProject))
        button2.pack()


class CreateNewProject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.variableProjectName = tk.StringVar()
        label = tk.Label(self, text="Experiment Name")
        label.pack(pady=10, padx=10)
        entry = tk.Entry(self, textvariable=self.variableProjectName)
        entry.pack()

        button1 = tk.Button(
            self,
            text="Create Experiment",
            command=lambda: self.getResponse(parent, controller, entry))
        button1.pack()

        button2 = tk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage))
        button2.pack()

    def getResponse(self, parent, controller, entry):
        projectName = self.variableProjectName.get()
        print(projectName)
        ld = LoadProject()
        ld.newProject(projectName)
        loadExisting = self.controller.get_page(LoadExistingProject)
        loadExisting.refreshOptions(self, parent)
        controller.show_frame(LoadExistingProject)


class LoadExistingProject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose Experiment")
        label.pack(pady=10, padx=10)

        lp = LoadProject()

        self.OPTIONS = lp.getProjects()

        self.variable_experiment_name = tk.StringVar(self)

        if len(self.OPTIONS) > 0:
            self.variable_experiment_name.set(self.OPTIONS[0])  # default value

        self.option = tk.OptionMenu(self, self.variable_experiment_name,
                                    *self.OPTIONS if self.OPTIONS else [0])
        self.option.pack()

        button1 = tk.Button(
            self,
            text="Load Experiment",
            command=lambda: self.getResponse(parent, controller))
        button1.pack()

    def refreshOptions(self, parent, controller):
        lp = LoadProject()
        self.option['menu'].delete(0, 'end')
        self.OPTIONS = lp.getProjects()
        for choice in self.OPTIONS:
            self.option['menu'].add_command(
                label=choice,
                command=tk._setit(self.variable_experiment_name, choice))
        if len(self.OPTIONS) > 0:
            self.variable_experiment_name.set(self.OPTIONS[0])  # default value

    def getResponse(self, parent, controller):
        print(self.variable_experiment_name.get())
        capture_pic_interface = self.controller.get_page(CapturePicInterface)
        capture_pic_interface.variable_experiment_name.set(self.variable_experiment_name.get())
        controller.show_frame(CapturePicInterface)


class CapturePicInterface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.variable_experiment_name = tk.StringVar()
        self.variable_id = tk.StringVar()
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.capture_rate = int(float(config['Camera']['capture_rate']) * 60)

        def callback():
            return True

        label_experiment_name = tk.Label(
            self,
            width=15,
            text="Experiment Name",
            anchor='w'
            ).grid(row=1)

        entry_experiment_name = tk.Entry(
            self,
            width=50,
            textvariable=self.variable_experiment_name,
            validate="focusout",
            # validatecommand=callback
            state='disabled',
        ).grid(row=1, column=1)

        label_id = tk.Label(
            self,
            width=15,
            text="ID (minutes)",
            anchor='w'
        ).grid(row=2)

        entry_id = tk.Entry(
            self,
            width=50,
            textvariable=self.variable_id,
        ).grid(row=2, column=1)

        labelImage = tk.Label(
            self,
            width=15,
            text="Image",
            anchor='w'
        ).grid(row=9)

        image = Image.new('RGB', (320, 256))
        image = image.resize((320, 256),
                             Image.LANCZOS)  # The (x, y) is (width, height)
        photo = ImageTk.PhotoImage(image)

        self.labelImage2 = tk.Label(self, image=photo, bg='gray')
        self.labelImage2.image = photo
        self.labelImage2.grid(row=9, column=1, padx=10, pady=10)

        self.buttonStart = tk.Button(
            self,
            bg='#9999ff',  # purpleish button
            text="Start",
            state='normal',
            command=lambda: self.start(parent, controller))
        self.buttonStart.grid(row=10, column=1, padx=10, pady=10)

        self.buttonStop = tk.Button(
            self,
            bg='#f58484',  # reddish button
            text="Stop",
            state='normal',
            command=lambda: self.stop())
        self.buttonStop.grid(row=10, column=2, padx=10, pady=10)

    def timer(self, parent, controller):
        if self.secs % self.capture_rate == 0:
            print(self.secs)
            self.getImage(parent, controller)
            self.variable_id.set(str(self.secs/60.0))
            self.getResponse(parent, controller)
        self.secs += 1
        self.after_id = self.after(1000, self.timer, parent, controller)  # Check again in 1 second.

    def start(self, parent, controller):
        self.secs = 0
        self.timer(parent, controller)  # Start repeated checking.

    def stop(self):
        print('stop')
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def getImage(self, parent, controller):
        cp = CapturePic()
        image = cp.capture_pic()

        self.image = Image.fromarray(image)
        imageSmall = self.image.resize(
            (320, 256), Image.LANCZOS)  # The (x, y) is (width, height)
        photo = ImageTk.PhotoImage(imageSmall)
        self.labelImage2.configure(image=photo)
        self.labelImage2.image = photo

    def getResponse(self, parent, controller):
        now = datetime.datetime.now()
        experiment_name = self.variable_experiment_name.get()[:-4]
        image_file_name = (experiment_name + '\\' + now.strftime('%Y_%m_%d_%H.%M.%S_') + experiment_name +
                           '_' + self.variable_id.get() + ".png")
        self.image.save(image_file_name)

        variables = [
            experiment_name,
            self.variable_id.get(),
            str(now),
            image_file_name
        ]

        ld = LoadProject()
        ld.saveData(self.variable_experiment_name.get(), variables)


app = App()
app.mainloop()
