# nfc-attendance
Attendance system powered by NFC module,
Created by Alp Sezer ORAK, under the internship project of Acibadem University

This project aims to create a new attendance system for Acibadem University, using their new university cards with NFC-chips to create an attendance system box.

The project works as follows,
1-) A recognized teacher reads their card and begins the attendance sequence
2-) A 10-minute timer begins
3-) During this 10-minute period, every student reads their card and if they're enrolled in the lecture's database, their attendance is taken, otherwise an error message is returned.

The project runs on MySQL and Python, using Adafruit PN532 RFID-NFC board.
