# Documentation <!-- omit from toc -->

## Table of contents <!-- omit from toc -->

- [Contributing](#contributing)
- [Installation and setup](#installation-and-setup)
  - [The main App](#the-main-app)
  - [Google API](#google-api)
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

## Contributing

1. Ensure you have Python installed.
2. Fork this repo.
3. Make a clone of the forked repo on your local machine.
4. In that clone, make changes, run tests, etc.
5. Push changes to your fork.
6. Issue a pull request and wait for me to review it.
7. If all goes well, I will merge your pull requests.
8. Please make sure your branch is always up-to-date with the main branch.

> [!NOTE]
> If this is your first time contributing to this project, please add your name to the [CONTRIBUTION.md](CONTRIBUTORS.md) file along with the date when you first joined. This is so that you guys all get acknowledged for your hard work.

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

        def Slot1(self):
            # Main thread's response to signal
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

Contain code for creating tokens for API operations such as creating a token, read and write to Google Sheets. Visit Google's [documentation](https://developers.google.com/sheets/api/guides/concepts) for a more detailed view and to familiarise yourself with the terminologies.

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
> The unique ID of a spreadsheet one wants to access.
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
> The unique ID of a spreadsheet one wants to access.
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

