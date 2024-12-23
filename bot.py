from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

BOT_TOKEN = "5166655063:AAGbUzz8cc3DmA95xE3Ch1Qnsl3N2qedVC0"  # Replace with your bot's token

# Function to handle files uploaded to the group
def handle_file(update: Update, context: CallbackContext):
    if update.message.document:  # Check if a document is sent
        file = update.message.document
        if file.file_name.endswith(".txt"):  # Ensure it's a .txt file
            # Download the file
            file_path = f"./{file.file_name}"
            file.download(file_path)
            update.message.reply_text(f"File {file.file_name} received and saved.")

            # Extract a specific line and save it to a new file
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Example: Extract the first line
            extracted_line = lines[0] if lines else "File is empty."

            # Save the extracted line to a new file
            new_file_path = f"extracted_{file.file_name}"
            with open(new_file_path, "w", encoding="utf-8") as f:
                f.write(extracted_line)

            # Send the new file back to the group
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(new_file_path, "rb"))

            # Clean up
            os.remove(file_path)
            os.remove(new_file_path)
        else:
            update.message.reply_text("Please upload a valid .txt file.")
    else:
        update.message.reply_text("No file detected. Please upload a .txt file.")

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a .txt file, and I'll extract lines for you!")

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
