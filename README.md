# JournalBot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

JournalBot is a Telegram bot developed using the aiogram library for chat management and the SQLAlchemy library for working with the database. This bot is designed to keep track of student attendance at study group classes.

## The bot's functionality includes:

1. Headman authentication: The headman enters his username, which is checked in the user database. After successful authentication, the bot identifies the prefect's study group and her full name.

2. Attendance mark:

* The headman can click the "Mark attendance" button, after which the bot asks him for a date in the format "dd.mm.yyyy".
* After entering the date, the bot provides a list of disciplines from the database and asks the prefect for a choice of discipline.
* The bot then requests the number of the pair in the schedule.
* After that, the bot displays a list of all students in the study group and asks the prefect to enter the numbers of missing students.
* The entered attendance information is saved in the database.

3. Viewing attendance:

* The headman can click the "View attendance" button, after which the bot gives the headman the opportunity to select a date and discipline.
* The bot then displays a list of students, noting those present and absent.
