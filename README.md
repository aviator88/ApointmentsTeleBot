A simple bot for scheduling an appointment with a specialist (doctor, psychologist, tutor, coach, etc.).
When first launched, it creates a database with the necessary tables. The first user to register is designated as the admin (the 'isAdmin' field = 1).
The admin can create and delete appointment slots and view recordings of upcoming appointments.
The user can view available appointment slots, schedule them, and cancel appointments.
The bot notifies the admin of new appointments in the chat, as it cannot message the admin directly. New appointments are checked every 10 minutes.
Once an hour, the bot deletes expired slots and appointments (records may not be deleted if the 'DELETE_OLD_APOINTMENT' parameter in the config.py file is set to 'False').
The following parameters must be specified in the .env file: 'BOT_TOKEN' - bot token, 'TECH_CHAT' - chat identifier for alerts.