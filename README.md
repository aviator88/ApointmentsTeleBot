# Appointments TeleBot

A Telegram bot for managing appointments with specialists (doctors, psychologists, tutors, coaches, etc.) with admin controls and user self-service booking.

## Features

- **Automatic Admin Assignment** - First registered user becomes the admin with full control
- **User Management** - Secure user registration with profile data (name, age, email, phone)
- **Appointment Slots** - Admins can create and delete appointment time slots
- **Self-Service Booking** - Users can view available slots and schedule appointments
- **Appointment Cancellation** - Users can cancel their bookings; admins can manage all appointments
- **Real-Time Notifications** - Admin receives instant alerts about new appointments via Telegram (checked every 10 minutes)
- **Automatic Cleanup** - Expired slots and appointments automatically deleted hourly
- **Persistent Storage** - SQLite database with automatic initialization
- **Async Performance** - Built with async/await for responsive interactions
- **Comprehensive Logging** - Debug logs for monitoring bot activity

## Getting Started

### Prerequisites

- Python 3.8+
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))
- Your Telegram Chat ID (for receiving admin alerts)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ApointmentsTeleBot.git
   cd ApointmentsTeleBot
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   
   Create a `.env` file in the project root:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   TECH_CHAT=your_chat_id_for_alerts
   ```
   
   **How to find your Chat ID:**
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - Use this as your `TECH_CHAT` value

5. **Run the bot**:
   ```bash
   python main.py
   ```
   
   The bot will automatically create `files/db.sql` with necessary database tables on first run.

### Usage

#### For New Users
1. Send `/start` to the bot
2. Complete the registration form (name, age, email, phone)
3. Access the user menu to view and book appointments

#### For Admins
- **First registered user automatically becomes admin**
- Create appointment slots (date and time)
- Delete slots and manage appointments
- Receive notifications about new bookings and cancellations

#### Commands
- `/start` - Open main menu
- `/cancel` - Cancel current action and return to menu

### Configuration Options

Edit `config.py` to customize behavior:

```python
DELETE_OLD_APOINTMENT = False  # Set to True to auto-delete expired appointments
```

Debug logs are saved to `files/debug.log` automatically.

## Project Structure

```
ApointmentsTeleBot/
├── main.py                      # Bot entry point and event loop
├── config.py                    # Configuration and logging
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── .github/prompts/             # Prompt instructions
├── auxiliary/                   # Core utilities
│   ├── classes.py              # Data models (User, Slot, Appointment)
│   ├── db.py                   # Database initialization
│   ├── forms.py                # User input FSM forms
│   ├── keyboard.py             # Telegram keyboard layouts
│   ├── messages.py             # Message templates
│   ├── checks.py               # Input validation
│   └── __init__.py
├── routers/                     # Command handlers
│   ├── start_router.py         # /start command and routing
│   ├── registration.py         # User registration flow
│   ├── admin_router.py         # Admin operations
│   ├── user_router.py          # User operations
│   └── __init__.py
└── files/                       # Data storage
    ├── db.sql                  # SQLite database (auto-created)
    └── debug.log               # Debug logs (auto-created)
```

## Technology Stack

- **[aiogram](https://docs.aiogram.dev/)** (3.25.0) - Async Telegram bot framework
- **[aiosqlite](https://aiosqlite.omnilib.dev/)** (0.22.1) - Async SQLite database
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** (1.2.1) - Environment variable management
- **[loguru](https://loguru.readthedocs.io/)** (0.7.3) - Structured logging
- **[pydantic](https://docs.pydantic.dev/)** (2.12.5) - Data validation

## Support

If you encounter issues:

1. **Check logs**: Review `files/debug.log` for detailed error information
2. **Verify configuration**: Ensure `.env` file has correct `BOT_TOKEN` and `TECH_CHAT`
3. **Test bot token**: Verify your token works with [@BotFather](https://t.me/botfather)
4. **Check permissions**: Ensure the bot can access your chat

## Contributing

Contributions are welcome! Please feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Suggest enhancements to user experience

## License

This project is licensed under the GNU General Public License v3.0 - see [LICENSE](LICENSE) file for details.

## Author

Created to simplify appointment scheduling for service providers and their clients.