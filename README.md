# Telegram Chat Moderator Bot
This repository contains the source code for a Telegram chat moderator bot developed using the Aiogram framework. The bot is capable of moderating an unlimited number of chats concurrently using a single bot instance.

## Functionality
### Message Filtering
The bot performs moderation of text messages in chats and provides the following functionality:

- Filtering of forbidden words: You can add forbidden words in both English and Russian languages. The bot will automatically delete messages containing these words. Symbol replacement is also supported, such as replacing "S" with "$" and "a" with "@" (about 500 symbols supported).

- Restriction on sending specific types of content: You can prohibit the sending of audio, photos, voice messages, videos, documents, text, geolocation, contacts, stickers, polls,animations, games, video notes, dices and venues. The bot will block attempts to send restricted content.

### Punishments
The bot also allows you to configure punishments for different types of violations. You can choose the following punishment options:

- Delete message: The bot will delete offending messages.

- Delete msg and block user: The bot will delete offending messages and block the user for some time.

You can also flexibly configure the duration of user blocks down to minutes, hours, and days. You can set up escalating block durations where each subsequent violation increases the block duration. One of the stages can be set as a warning.

### Restricted Functionality during Blocking
You can customize the availability of specific functions during user blocking. By default, all functions will be unavailable, but you can change this in the settings.

### Sending Messages after Blocking
You can configure whether the bot should send messages to the general chat after blocking a user. You can easily modify the text of these messages in the *textsConfig.py* file.

### Statistics and Logging
The bot provides the ability to view detailed statistics and logs all blocks, warnings, and other actions. Logs can be accessed directly in the bot's admin panel.

## Usage
To run the bot locally, follow these steps:

1) Install the dependencies using the command pip install -r requirements.txt.

2) Fill in the *config.py* file with the necessary parameters. In this file, you can configure the main bot parameters, such as the Telegram API token, ban steps, and other important parameters.

3) Run the main.py file to start the bot.

## Commands
- **/start**: This command provides a placeholder for regular users.

- **/admin**: This command grants administrators access to almost all bot settings. Administrators can configure fundamental bot parameters that are not intended to be changed during runtime.

- **/unban <user_id>**: This command removes all restrictions from a user in the chat prematurely.

## Configuration
Bot settings are configured in the *config.py* file. In this file, you can customize various bot parameters, including the Telegram API token, database settings, content restrictions, punishment settings, and other parameters.

## License
This project is licensed under the MIT License. For more information, see the *LICENSE* file.