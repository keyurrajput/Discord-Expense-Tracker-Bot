# Discord Expense Tracker Bot

A personal finance bot that turns your Discord DMs into a simple expense management system. Send expenses like "150, lunch" or "45, samosa, bikaner" and they're instantly logged to Google Sheets with timestamps.

## Features

- **Simple Expense Tracking**: Just send a message like `150, lunch` or `45, samosa, bikaner`
- **Automatic Categorization**: Format separates amount, item, and place
- **Google Sheets Integration**: All expenses are saved to your own spreadsheet
- **Private DM Interface**: Track expenses through direct messages
- **Helpful Commands**: Check totals and today's expenses easily

## Getting Started

### Prerequisites

- Python 3.6+
- A Discord account
- A Google account

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/discord-expense-tracker.git
   cd discord-expense-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install discord.py gspread oauth2client python-dotenv
   ```

3. **Create a Discord bot**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" tab and click "Add Bot"
   - Under "Privileged Gateway Intents", enable "Message Content Intent" and "Server Members Intent"
   - Copy your bot token for the next step

4. **Set up Google Sheets API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Sheets API and Google Drive API
   - Create Service Account credentials
   - Download the JSON credentials file and save it as `credentials.json` in your project directory

5. **Create a `.env` file**
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

6. **Invite the bot to a server**
   - Go to OAuth2 > URL Generator in the Discord Developer Portal
   - Select "bot" under "SCOPES"
   - Select at minimum: "Send Messages" and "Read Message History" permissions
   - Copy and open the generated URL to invite the bot to a server you manage
   - You need to share at least one server with the bot to DM it

### Running the Bot

```bash
python bot.py
```

## Usage

Once the bot is running, you can start tracking expenses:

1. **Open Discord** and send a direct message to your bot
2. **Track an expense** by sending a message in one of these formats:
   - `amount, item` (e.g., "150, lunch")
   - `amount, item, place` (e.g., "45, samosa, bikaner")

3. **Use commands** in your DMs with the bot:
   - `!total` - See the sum of all expenses
   - `!today` - See today's expenses with breakdown
   - `!help` - Get usage instructions

## Example Usage

```
You: 150, lunch
Bot: 💰 Expense tracked: ₹150 for lunch

You: 45, samosa, bikaner
Bot: 💰 Expense tracked: ₹45 for samosa at bikaner

You: !today
Bot: **Today's Expenses:**
₹150 - lunch (N/A)
₹45 - samosa (bikaner)

**Total:** ₹195.00
```

## Google Sheet Structure

The bot creates a Google Sheet with the following columns:
- **Timestamp**: Exact time of the expense entry
- **Date**: Just the date portion
- **Amount**: The expense amount
- **Item**: What was purchased
- **Place**: Where it was purchased (if provided)

## Customization

You can modify the `bot.py` file to:
- Change the sheet name by updating `SHEET_NAME`
- Add more commands for different expense analyses
- Customize confirmation messages

## Troubleshooting

**Bot doesn't respond to DMs**
- Make sure you've invited the bot to a server you're in
- Check that you've enabled "Message Content Intent" in the Discord Developer Portal
- Verify your bot token is correct in the `.env` file

**Can't connect to Google Sheets**
- Check that your `credentials.json` file is in the project directory
- Ensure the Google Sheets API and Google Drive API are enabled
- Verify the service account has proper permissions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [discord.py](https://discordpy.readthedocs.io/)
- Uses [gspread](https://gspread.readthedocs.io/) for Google Sheets integration