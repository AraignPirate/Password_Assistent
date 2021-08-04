<div align="center"><img  style="height:70px;width:70px;" src="https://github.com/AraignPirate/Password_Assistent/blob/main/Appfiles/Icon.png" alt="Password Assistent Icon"/></div>
<h1 align="center">Password Assistent</h1>

## About
This is a Python Software to store **credentials**.
- Python project build with
  - ***Python (3.9.5)***
  - ***kivy/kivyMD (for GUI)***

It Has multi-users functionalities and can store passwords for different users.

All Credentials are encrypted with a unique key for each.

See all wifi Credentials stored on your system.

**TESTED ON** : Linux (Debian) , Windows 10

**DEVELOPED ON** : kali Linux 

## Features
- Stores site/comment,username,password 
  - It will also try to download site icon if the site is valid.
- Shows stored wifi passwords on system
- Generate Strong Passwords

## Instalation Setup
Required **Python version (3.9.5)**

#### Clone the repo 
- run this command or download as a zip.
- > `git clone https://github.com/AraignPirate/Password_Assistent.git`

#### Install Dependencies
- run these command in *terminal/cmd*
- > `cd Password_Assistent`
- > `python3 -m pip install -r Appfiles/requirments.txt`
- Alternate way to install dependencies
- > `pip3 install -r Appfiles/requirements.txt`

## Run Password_Assistent.py
- run the script using *python* on *terminal/cmd*
- > `python3 Password_Assistent.py`

## Software Demo
After running the script this software will **check/create** required files on its **first run**

- If All the Files are there then it will open a ***login screen***.

!["App's Login Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/Login_screen.png)

- As until now we did'nt have any user. To create User click on **"forgot your password ?"** and then choose **"Register ?"** from the next Screen.

!["App's Register Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/Register_Screen.png)

- Fill all the required fields to register in this app. After that you will get redirected to **Login Screen** enter your credentials and click on login.
- If login is successfull then you will be on **Dashboard screen**.

!["App's Dashboard Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/Dashboard.png)

- From Dashboard screen you can ***store and generate password***.
  - To store password click on ***"Add Password"*** and fill all the fields.
- To Generate Password click on ***"Generate Password"*** it will open new screen like this 

!["App's Generate Password Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/Generate_pass_screen.png)

- Set Required Password custom settings and click on **"Generate"**
- A password list will open, click on the password you like it will get coppied to clipboard.

!["App's Generate Password copy  Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/copy_pass.png)

- From **Menu** Button you can access the Navigation Slider to switch between Screens.

!["App's Nav Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/Nav-Bar.png)

- **Wifi Auths** Screen will show all wifi passwords stored on system.

!["App's Wifi Auth Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/Wifi_auth.png)

- **Settings** Screen controls logging of application.
  - Default Setting Logs to **file**
  - Other Settings Logs to **terminal/cmd**

!["App's Settings Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/Log_settings.png)

- **About** Screen just defines the app.

!["App's Settings Screen"](https://github.com/AraignPirate/Password_Assistent/blob/main/Demo/about.png)

## Video Demo

Video demo is present in `Demo/Video_demo.mp4`
