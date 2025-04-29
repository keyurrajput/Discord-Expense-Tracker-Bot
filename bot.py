import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord bot setup - we need to use different intents for DMs
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# Google Sheets setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'credentials.json'
SHEET_NAME = 'Expense Tracker'

# Connect to Google Sheets
def connect_to_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    
    # Open the sheet - create if it doesn't exist
    try:
        sheet = client.open_by_key("1KwcBHI5rDnHKCZb6b6aYbaQNEaSM-YgvxUSI_xDEhJ8").sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = client.open_by_key("1KwcBHI5rDnHKCZb6b6aYbaQNEaSM-YgvxUSI_xDEhJ8").sheet1
        # Add headers
        sheet.append_row(['Timestamp', 'Date', 'Amount', 'Item', 'Place'])
    
    return sheet

@bot.event
async def on_ready():
    print(f'{bot.user} is connected and ready!')
    
    # Connect to Google Sheets on startup
    global sheet
    try:
        sheet = connect_to_sheets()
        print("Connected to Google Sheets successfully!")
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Only process DMs (not server messages)
    if not isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)
        return
    
    # Check if the message is a command
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return
    
    # Process the expense message
    try:
        parts = [part.strip() for part in message.content.split(',')]
        
        # Prepare data based on message format
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Parse the message based on number of parts
        if len(parts) == 2:  # Format: amount, item
            amount = float(parts[0])
            item = parts[1]
            place = ""
        elif len(parts) >= 3:  # Format: amount, item, place
            amount = float(parts[0])
            item = parts[1]
            place = parts[2]
        else:
            # Invalid format
            await message.channel.send("❌ Invalid format. Please use: `amount, item` or `amount, item, place`")
            return
        
        # Add to Google Sheet
        row = [timestamp, date, amount, item, place]
        sheet.append_row(row)
        
        # Send confirmation
        await message.add_reaction("✅")
        await message.channel.send(f"💰 Expense tracked: ₹{amount} for {item}" + (f" at {place}" if place else ""))
        
    except ValueError:
        await message.channel.send("❌ Invalid amount. The first value must be a number.")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

@bot.command(name='total')
async def show_total(ctx):
    """Shows the total expenses"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    try:
        # Get all values from column C (Amount)
        amounts = sheet.col_values(3)[1:]  # Skip header
        if not amounts:
            await ctx.send("No expenses recorded yet!")
            return
        
        # Convert to float and sum
        total = sum(float(amount) for amount in amounts)
        await ctx.send(f"💵 Total expenses: ₹{total:.2f}")
    except Exception as e:
        await ctx.send(f"❌ Error calculating total: {str(e)}")

@bot.command(name='today')
async def today_expenses(ctx):
    """Shows today's expenses"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    try:
        # Get all rows
        all_rows = sheet.get_all_values()[1:]  # Skip header
        if not all_rows:
            await ctx.send("No expenses recorded yet!")
            return
        
        # Filter for today's date
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_expenses = []
        today_total = 0
        
        for row in all_rows:
            if row[1] == today:  # Check the Date column
                amount = float(row[2])  # Amount column
                item = row[3]  # Item column
                place = row[4] if row[4] else "N/A"  # Place column
                
                today_expenses.append(f"₹{amount} - {item} ({place})")
                today_total += amount
        
        if not today_expenses:
            await ctx.send("No expenses recorded today!")
            return
            
        # Create the response
        response = "**Today's Expenses:**\n" + "\n".join(today_expenses)
        response += f"\n\n**Total:** ₹{today_total:.2f}"
        
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"❌ Error retrieving today's expenses: {str(e)}")

@bot.command(name='expense_help')
async def expense_help_command(ctx):
    """Shows help information"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    help_text = """
**Expense Tracker Bot Help**

To track an expense, simply message me in this format:
`amount, item` or `amount, item, place`

Examples:
`150, Lunch`
`45, AI - Samosa, Sion`

**Commands:**
`!total` - Show total expenses
`!today` - Show today's expenses
`!help` - Show this help message
    """
    await ctx.send(help_text)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))