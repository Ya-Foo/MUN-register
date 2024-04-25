# Documentation <!-- omit from toc -->

## Table of contents <!-- omit from toc -->

- [Contributing](#contributing)
- [Installation and setup](#installation-and-setup)
  - [The main App](#the-main-app)
  - [Google API](#google-api)
  - [Testing environment](#testing-environment)
- [App architecture and mechanisms](#app-architecture-and-mechanisms)
  - [Threading theory](#threading-theory)
    - [Main thread](#main-thread)
    - [Worker thread](#worker-thread)
  - [Threading implementation](#threading-implementation)
- [App GUI](#app-gui)
- [Code organisation](#code-organisation)
  - [api.py](#apipy)
  - [app.py](#apppy)
  - [end.py](#endpy)
  - [attendance.py](#attendancepy)
  - [qrRead.py](#qrreadpy)
  - [chairing.py](#chairingpy)
  - [speech.py](#speechpy)
  - [timer.py (not done)](#timerpy-not-done)
  - [vote.py](#votepy)
  - [managing.py](#managingpy)
  - [homework.py](#homeworkpy)
  - [qrCreate.py](#qrcreatepy)
  - [wiki.py (not done)](#wikipy-not-done)
  - [settings.py (not done/in progress)](#settingspy-not-donein-progress)
  - [config.json](#configjson)
    - [General config](#general-config)
    - [info](#info)
    - [session](#session)
    - [management](#management)

## Contributing

> [!NOTE]
> If this is your first time contributing to this project, please add your name to the [CONTRIBUTION.md](CONTRIBUTORS.md) file along with the date when you joined this project and your GitHub username. This is so that you guys all get acknowledged for your hard work.

1. Ensure you have Python and Git installed.
2. Create a GitHub account if not already done so.
3. Fork this repo.
4. Make a clone of the forked repo on your local machine.
5. In that clone, make changes, run tests, etc.
6. Push changes to your fork.
7. Issue a pull request and wait for me to review it.
8. If all goes well, I will merge your pull requests.

> [!IMPORTANT]
> Please make sure your branch is always up-to-date with the main branch.  
> Also please write the documentation for any code you wrote.

## Installation and setup

### The main App

Once you have this project on your local machine:

1. Change to project directory  

    ```shell
    cd MUN-register
    ```

2. (Optional) Install virtual environment

    ```powershell
    python -m venv env
    env/Scripts/activate
    ```

3. Install library dependencies

    ```powershell
    python -m pip install -r requirements.txt
    ```

4. Create directory for authentication details
  
   ```powershell
   md auth
   ```

### Google API

> [!IMPORTANT]
> This is only used only for features which involves reading and writing data onto the BISMUN Google Sheet.  
> Regardless, you should still get this set up step done.

Download the `.env` file I sent you and put it in `/auth`.

Alternatively, you can create your own credentials using the guidelines from Google [here](https://developers.google.com/workspace/guides/get-started). Make sure you enable Google Sheets API when enabling Google Workspace APIs and choose OAuth 2.0 for authorization. Finally convert your `credentials.json` to `credentials.env`.

> [!CAUTION]
> DO NOT share these files to anyone, nor put it on a public repository as it will cause security risks to your account.

### Testing environment

1. Navigate to `config.json`
2. Visit this [spreadsheet](https://docs.google.com/spreadsheets/d/1UT_GerjzJCv7Bu_MnEMHZUr533mF3xe0W0rMiUlHnq4/edit#gid=0), which have been formatted exactly like the spreadsheet used by chairs.
3. Paste the URL of the sheet into the key `sheets_url`'s value.
4. Change `register_column`, `speech_column`, `amendment_column`, and `poi_column` value to G, H, I, J, respectively.
5. Save the file, and run the app.
6. If there is a Google sign-in prompt, please sign in using the @bisvietnam.com account.

## App architecture and mechanisms

### Threading theory

The library used to create this app is PyQt5. They provide their own infrastructure to create multithreaded applications using `QThread`. There are two main kinds of Thread:

1. Main thread
2. Worker threads

#### Main thread

The Main thread is essentially the main application and its GUI run. It runs after the `.exec()` function is called on the `QApplication` object. Any tasks or events that takes place in this thread, including the user's interaction with the GUI, will run **synchronously** (one tasks after another). So, if you start a long-running task in the main thread, then the application needs to wait for that task to finish, and the GUI becomes unresponsive.

#### Worker thread

You can create as many worker threads as you need in your PyQt applications. Worker threads are secondary threads of execution that are used to process other heavy tasks which might freeze the main GUI (for example, in our case, extracting information from camera or sending HTTPs requests to Google Sheets).

We use the results from these worker threads and feed it back to the Main thread in their designated slots. Basically, the Main thread is used to display the results and the Worker threads will do most of the weight-lifting.

To communicate with the Main thread (i.e to tell it what to display), we use a signal-slot approach. The Main thread will have slots for each different signal. These are essentially functions/procedure which get called everytime a signal response is received. Each worker thread may have one or more signals, each is assigned the datatype which they can emit. When the worker thread emit that signal, they will tell the Main thread to activate the associated slots and react to the signal. There is no need to create signals and slots if the worker thread will not send anything back to the Main thread.

See diagram below to visualise this:

### Threading implementation

1. Create a worker class

    ```python
    class WorkerName(QThread):
        # Initialise, if any, signals
        signalName = pyqtSignal(datatype)

        def __init__(self, anyinputparamter) -> None:
            super(WorkerName, self).__init__()

            # declare any attributes here
            self.attribute = ... 

        def run(self) -> None:
            # Put the long-running tasks here
    ```

2. Defining signals

    ```python
    self.signalName.emit(data)
    ```

3. Creating and connecting slots in Main thread

    ```python
    class MainThread(QApplication):
        def __init__(self):

            [...]

            # Create worker instance
            self.Thread1 = WorkerName()
            # Start the worker/thread
            self.Thread1.start()
            # Connecting signal to slot
            self.Thread1.signalName.connect(self.Slot1)

        [...]

        def Slot1(self, received_value):
            # Main thread's response to signal
            # received_value is the same datatype as the signal.
    ```

4. Ending a worker thread

    ```python
    self.quit()
    ```

    or

    ```python
    self.Thread1.quit()
    ```

There are many more things you can do with Threads, just visit the [PyQt5 documentation](https://doc.qt.io/qtforpython-5/) to find out more.

## App GUI

Gia Phu and Henry have already designed the GUI so follow their designs [here](https://docs.google.com/presentation/d/1qY5cqMBw-6FbdSAbfHJeYvB0jWfJhM9Rk-8UDwVV-hQ/edit#slide=id.g2c20d570521_0_10). If you do not have access, change to @bisvietnam.com account.

To grasp the basics of creating GUI with PyQt5, please have a read through [this](https://www.pythonguis.com/tutorials/pyqt-basic-widgets/) and [this](https://www.pythonguis.com/tutorials/pyqt-layouts/), in that order. In a short summary, the process of adding GUI elements includes:

1. Create a layout
2. Define a widget
3. Customise the widget
4. Add that widget to the layout
5. Set and finalise layout
6. Show the widget / main thread

For any web-devs out there, this is very similar to HTML and CSS, where the Main application is the `<body>` and the widgets are `<div>` elements; both can be customised with a language similar to CSS.

## Code organisation

```text
src
|   api.py
|   app.py
|   end.py
|   
+---attendance
|       attendance.py
|       qrRead.py
|       __init__.py
|       
+---chairing
|       chairing.py
|       speech.py
|       timer.py
|       vote.py
|       __init__.py
|       
+---management
|       homework.py
|       managing.py
|       qrCreate.py
|       wiki.py
|       __init__.py
|       
\---settings
        config.json
        settings.py
        __init__.py
```

### api.py

Contain code for creating tokens for API operations such as creating a token, read and write to Google Sheets. Visit Google's [documentation](https://developers.google.com/sheets/api/guides/concepts) for a more detailed view and to familiarise yourself with the terminologies. Every read/write operations will be done on a worker thread because they usually take very long to accomplish.

`auth()`  
Return a credential from token for end-user to access the Google Sheets. If there is no token, it will create a token file based on the user's API credentials.
> Parameters:
>
> - None
>
> Returns:
>
> - cred : Any  
> The credential is used to authorize read and write operations from the app.

`get_values(creds, spreadsheet_id, range_name)`  
Return data obtained from the specified Google Sheets range.
> Parameters:
>
> - creds : Any  
> Credential token obtained from `auth()`.
>  
> - spreadsheet_id : str  
> The unique ID of a spreadsheet one wants to access. Parsed from the URL in the config.json
>  
> - range_name : str  
> A Google Sheet range to get data from.
>
> Returns:
>
> - rows : a [ValueRange](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#resource-valuerange) object
> - error : HttpError

`write_values(creds, spreadsheet_id, range_name, value_input_option, value)`  
Write data to a single range.
> Parameters:
>
> - creds : Any  
> Credential token obtained from `auth()`.
>  
> - spreadsheet_id : str  
> The unique ID of a spreadsheet one wants to access. Parsed from the URL in the config.json
>  
> - range_name : str  
> A Google Sheet range to get data from.
>  
> - value_input_option : str  
> How the input data should be interpreted. See [here](https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption) for options.
>  
> - value : str  
> The value that will be entered into the cells.
>
> Returns:
>
> - error : HttpError

### app.py

Where the Main thread is coded and run.

### end.py

Code for the exit window of the program.

`ExitWindow`  
A QWidget class/object that will allow the user to end the session and update information for next week if needed be.

`yes(self)`  
A procedure which updates config.json upon exiting the program.

`increaseCol(x)`  
A function which returns the new column for next session.

> Parameters:
>
> - x : str  
> A string that represents the current column for data entry.
>  
> Returns:
>
> - new_col : str  
> A string that represents the column for data entry for next session.

---

### attendance.py

Code concerning displaying the GUI for attendance-related tasks.

`Attendance`  
A QWidget class/object that displays camera feed and scanned information.

### qrRead.py

Code concerning the reading, processing, and updating information from camera feed.

`QRRead(QThread)`  
A worker thread which captures video and detects QR code.

> Parameters:
>
> - None
>
> Signals:
>
> - ImageUpdate : QImage  
> Sends out copies of what the camera is capturing after converting from numpy array to QImage. This must be done for all images that needs to be displayed with PyQt5.
>
> - InfoUpdate : str  
> Emits the data read from any QR code detected. A valid BISMUN QR code will have the delegate's identifier encoded in it.
>
> - NameUpdate : str  
> Emits the delegate's full name extracted from a dictionary using the identifier as key.

`Register(QThread)`  
A worker thread which takes output from `QRRead` and update the Google Sheet accordingly.

> Parameters:
>
> - identifier : str  
> The value emitted from the InfoUpdate signal from the QRRead.
>
> Signals:
>
> - None

---

### chairing.py

Code concerning displaying the GUI for chairing-related tasks.

`Chairing`  
A QWidget class/object that displays processes or tasks that concern with chairing such as vote counting and marking conference contributions.

### speech.py

Code concerning the recording of speeches, POI, and amendments.

`RecordWidget`  
A QWidget that allow chairs to select what kind of contribution (speeches, poi, amendments) that a delegate make and then record it onto the Google Sheets.

`RecordEngagement(QThread)`  
A worker thread which takes the chair's input (from the drop-down menu) and write those data onto the Google Sheets. It will also display the options that the chairs have (such as list of countries in the room) upon selecting.
> Parameters:
>
> - room : str  
> The room the chair is chairing in. All the possible options is in the config.json
>
> - country (for the run method) : str  
> The country which made the contribution. All the possible options is extracted from the corresponding tab in the Google Sheets.
>
> - speechType (for the run method) : str  
> The type of contribution the delegate made (speech, amendments, poi)
>
> Signals:
>
> - None

### timer.py (not done)

Code concerning the timer chairs can use to time delegate's speeches.

### vote.py

Code concerning with the counting of votes and displaying the results of that voting.

`VoteWidget`  
A QWidget which displays the vote-counting functions, as well as providing the mechanism behind vote calculations (with simple and supermajority taken into account).

---

### managing.py

Code concerning the management and admin stuff that chairs will do, including homework recording, generating QR codes and fact-checking.

`Managing`  
A QWidget class/object that displays the GUI for processes or tasks concerning admin and management.

### homework.py

Code concerning with recording the completion of homework (ie: researching and drafting resolutions).

`HomeworkWidget`  
A QWidget which displays the drop-down menu for chairs to mark homework completion. It has the following options: delegate's name, tasks, and status.

`RecordHomework(QThread)`  
A worker thread which takes inputs from the drop-down menus and record it appropriately onto the Google Sheets.
> Parameters:
>
> - name_list : 1D list  
> List of all the delegate's name. Extracted from the Google Sheets.
>
> - name : str  
> The delegate's name. Possible options are in the name_list parameter.
>
> - homework : str  
> The type of homework the chair wants to mark. Currently there are two options: research and resolution drafting.
>
> - status : str  
> Completion status. All the possible status is in the config.json
>
> Signals:
>
> - None

### qrCreate.py

Code that concerns with the QR creation processes. Chairs can create QR codes for individual or create everything at once.

`QRCreateWidget`  
A QWidget which has all the drop-down menus for the QR creation. It acts as a form which allow chairs to submit QR creation requests to their computers and let it cook.

`QRCreate(QThread)`  
A worker thread which takes input from the drop-down lists in `QRCreateWidget` and produces the correct QR codes in the designated directory in response.
> Parameters:
>
> - option : int  
> The index of the chosen item in the drop-down menu of options. This will allow the worker to know which QR code to produce.
>
> Signals:
>
> - None

### wiki.py (not done)

Code that allow chairs to quickly search information on the Wikipedia Encyclopedia and displaying the results for fact-checking.

---

### settings.py (not done/in progress)

Code that extract all the confirgurations from config.json and also allow the chairs to change those configurations which is then updated accordingly.

### config.json

```json
{
    "camera_id": 0,
    "sheets_url": "www.url-to-google-sheets.com/idk/what/are/you/doing",
    "present_marker": "/",

    "info": {
        "page": "delegatesInfo",
        "start_row": 1
    },

    "session": {
        "rooms": [
            "Room 1",
            "Room 2"
        ],
        "identifier_column": "C",
        "country_column": "B",
        "register_column": "G",
        "speech_column": "H",
        "amendment_column": "I",
        "poi_column": "J",
        "start_row": 3
    },

    "management": {
        "sheet": "Task Completion",
        "start_row": 2,
        "name_column": "A",
        "research_column": "B",
        "speech_column": "C",
        "status": [
            "/",
            "unwritten",
            "late",
            "/ but unsubmitted",
            "excused",
            "notified"
        ]
    }
}
```

#### General config

The first three attributes of `config.json`.

| Attribute         | Meaning                                                          |
|-------------------|------------------------------------------------------------------|
| camera_id         | 0 (default) for webcam or 1 for back cam                         |
| sheets_url        | The URL of the Google Sheets used for attendance                 |
| present marker    | The text character that is used by the club to indicate presence |

#### info

The attributes within `"info": {...}`.

| Attribute         | Meaning                                                  |
|-------------------|----------------------------------------------------------|
| page              | The name of the sheet where the info is located          |
| start_row         | The row containing the first delegate                    |

#### session

The attributes within `"session": {...}`.

| Attribute         | Meaning                                                         |
|-------------------|-----------------------------------------------------------------|
| rooms             | The name of the sheet where the info is located                 |
| identifier_column | The column in which the delegates' identifiers are placed       |
| country_column    | The column in which the delegates' allocated country are placed |
| register_column   | The column in which attendance will be marked                   |
| speech_column     | The column in which speech contributions are marked             |
| amendment_column  | The column in which amendment contributions are marked          |
| poi_column        | The column in which poi contributions are marked                |
| start_row         | The row containing the first delegate                           |

#### management

The attributes within `"management": {...}`.

| Attribute         | Meaning                                                           |
|-------------------|-------------------------------------------------------------------|
| sheet             | The name of the sheet where the info is located                   |
| start_row         | The row containing the first delegate                             |
| name_column       | The column containing delegate's names                            |
| research_column   | The column in which research homeworks are marked                 |
| speech_column     | The column in which resolution drafting homeworks are marked      |
| status            | All of the possible homework completion status                    |
