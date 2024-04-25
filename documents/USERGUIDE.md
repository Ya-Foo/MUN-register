# User guide <!-- omit from toc -->

## Table of contents <!-- omit from toc -->

- [Installations](#installations)
  - [Manual](#manual)
  - [Windows](#windows)
  - [macOS](#macos)
- [Execution](#execution)
  - [Initial configuration](#initial-configuration)
  - [Running the app](#running-the-app)

## Installations

1. [Download](https://github.com/Ya-Foo/MUN-register/archive/refs/heads/main.zip) this repository as a .zip file. If the link does not work, click the green button which says **<> Code** on the top-right, then click **Download ZIP**.
2. Unzip the file to an appropriatedly named folder.
3. Email the Chief of Technical Advisor for the credentials.
4. Choose the method through which you want to install your app, then find and follow the appropriate guide below.

### Manual

1. Install Python through this [link](https://www.python.org/downloads/).
2. Install library dependencies.

    ```powershell
    python -m pip install -r requirements.txt
    ```

3. Change to project directory then create a sub-directory for authentication details.

    ```shell
    cd MUN-register
    md auth
    ```

4. Move the credentials into the directory you just created.

### Windows

### macOS

## Execution

### Initial configuration

### Running the app

`python src/app.py`
