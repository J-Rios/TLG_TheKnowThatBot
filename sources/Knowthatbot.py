# -*- coding: utf-8 -*-
'''
Script:
    Knowthatbot.py
Description:
    Telegram Bot to request info about anything and it search and response with the first Wikipedia 
    sentence of that thing.
Author:
    Jose Rios Rubio
Creation date:
    16/06/2018
Last modified date:
    01/07/2018
Version:
    1.1.0
'''

####################################################################################################

### Imported modules ###
import wikipedia
from Constants import CONST, TEXT
from TSjson import TSjson
from sys import exit
from signal import signal, SIGTERM, SIGINT
from os import path, makedirs, listdir
from datetime import datetime, timedelta
from time import time, sleep, strptime, mktime
from threading import Lock
from operator import itemgetter
from collections import OrderedDict
from uuid import uuid4
from telegram import ParseMode, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler

####################################################################################################

### Globals ###
files_config_list = []
to_delete_messages_list = []

####################################################################################################

### Termination signals handler for program process ###

def signal_handler(signal, frame):
    '''Termination signals (SIGINT, SIGTERM) handler for program process'''
    print('Closing the program, safe way...')
    # Acquire all messages and users files mutex to ensure not read/write operation on them
    for chat_users_file in files_users_list:
        chat_users_file['File'].lock.acquire()
    for chat_messages_file in files_messages_list:
        chat_messages_file['File'].lock.acquire()
    # Close the program
    exit(0)


# Signals attachment
signal(SIGTERM, signal_handler) # SIGTERM (kill PID) to signal_handler
signal(SIGINT, signal_handler)  # SIGINT (Ctrl+C) to signal_handler

####################################################################################################

### Auxiliar functions ###

def initialize_resources():
    '''Initialize resources by populating files list with chats found files'''
    global files_config_list
    # Create data directory if it does not exists
    if not path.exists(CONST['DATA_DIR']):
        makedirs(CONST['DATA_DIR'])
    else:
        # If directory data exists, check all subdirectories names (chats ID)
        files = listdir(CONST['DATA_DIR'])
        if files:
            for f in files:
                # Restore last configurations properties of the chat
                config_file = OrderedDict([('ID', f), ('File', get_chat_config_file(f))])
                files_config_list.append(config_file)


def get_chat_config_file(chat_id):
    '''Determine chat config file from the list by ID. Get the file if exists or create it if not'''
    file = OrderedDict([('ID', chat_id), ('File', None)])
    found = False
    if files_config_list:
        for chat_file in files_config_list:
            if chat_file['ID'] == chat_id:
                file = chat_file
                found = True
                break
        if not found:
            chat_config_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_CONF'])
            file['ID'] = chat_id
            file['File'] = TSjson(chat_config_file_name)
            files_config_list.append(file)
    else:
        chat_config_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_CONF'])
        file['ID'] = chat_id
        file['File'] = TSjson(chat_config_file_name)
        files_config_list.append(file)
    return file['File']


def get_default_config_data():
    '''Get default config data structure'''
    config_data = OrderedDict( \
    [ \
        ('Language', CONST['INIT_LANG']), \
        ('Enable', CONST['INIT_ENABLE'])
    ])
    return config_data


def save_config_property(chat_id, property, value):
    '''Store actual chat configuration in file'''
    file = get_chat_config_file(chat_id)
    config_data = file.read()
    if not config_data:
        config_data = get_default_config_data()
    config_data[property] = value
    file.write(config_data)


def get_chat_config(chat_id, param):
    '''Get specific stored chat configuration property'''
    file = get_chat_config_file(chat_id)
    if file:
        config_data = file.read()
        if not config_data:
            config_data = get_default_config_data()
    else:
        config_data = get_default_config_data()
    return config_data[param]


def user_is_admin(bot, user_id, chat_id):
    '''Check if the specified user is an Administrator of a group given by IDs'''
    try:
        group_admins = bot.get_chat_administrators(chat_id)
    except:
        return None
    for admin in group_admins:
        if user_id == admin.user.id:
            return True
    return False


def bot_is_admin(bot, chat_id):
    '''Check if the Bot is Admin of the actual group'''
    try:
        bot_id = bot.id
        group_admins = bot.get_chat_administrators(chat_id)
    except:
        return None
    for admin in group_admins:
        if bot_id == admin.user.id:
            return True
    return False


def tlg_send_selfdestruct_msg(bot, chat_id, message):
    '''tlg_send_selfdestruct_msg_in() with default delete time'''
    tlg_send_selfdestruct_msg_in(bot, chat_id, message, CONST['T_DEL_MSG'])


def tlg_msg_to_selfdestruct(bot, message):
    '''tlg_msg_to_selfdestruct_in() with default delete time'''
    tlg_msg_to_selfdestruct_in(bot, message, CONST['T_DEL_MSG'])


def tlg_send_selfdestruct_msg_in(bot, chat_id, message, time_delete_min):
    '''Send a telegram message that will be auto-delete in specified time'''
    # Send the message
    sent_msg = bot.send_message(chat_id, message)
    # If has been succesfully sent
    if sent_msg:
        # Get sent message ID and delete time
        msg_id = sent_msg.message_id
        destroy_time = int(time()) + int(time_delete_min*60)
        # Add sent message data to to-delete messages list
        sent_msg_data = OrderedDict([('Chat_id', None), ('Msg_id', None), ('delete_time', None)])
        sent_msg_data['Chat_id'] = chat_id
        sent_msg_data['Msg_id'] = msg_id
        sent_msg_data['delete_time'] = destroy_time
        to_delete_messages_list.append(sent_msg_data)


def tlg_msg_to_selfdestruct_in(bot, message, time_delete_min):
    '''Add a telegram message to be auto-delete in specified time''' 
    # Get sent message ID and delete time
    chat_id = message.chat_id
    msg_id = message.message_id
    destroy_time = int(time()) + int(time_delete_min*60)
    # Check if the Bot is Admin
    if bot_is_admin(bot, chat_id) == True:
        # Add sent message data to to-delete messages list
        sent_msg_data = OrderedDict([('Chat_id', None), ('Msg_id', None), ('delete_time', None)])
        sent_msg_data['Chat_id'] = chat_id
        sent_msg_data['Msg_id'] = msg_id
        sent_msg_data['delete_time'] = destroy_time
        to_delete_messages_list.append(sent_msg_data)


def selfdestruct_messages(bot):
    '''Handle remove messages sent by the Bot with the timed self-delete function'''
    global to_delete_messages_list
    while True:
        # Check each Bot sent message
        for sent_msg in to_delete_messages_list:
            # If actual time is equal or more than the expected sent msg delete time
            if int(time()) >= sent_msg['delete_time']:
                # Try to delete that sent message if possible (still exists)
                try:
                    if bot.delete_message(sent_msg['Chat_id'], sent_msg['Msg_id']):
                        to_delete_messages_list.remove(sent_msg)
                except Exception as e:
                    #print("Error: {}".format(e.message)) # i.e. "Message to delete not found"
                    to_delete_messages_list.remove(sent_msg)
        # Wait 10s (release CPU usage)
        sleep(10)

####################################################################################################

### Received Telegram command messages handlers ###

def cmd_start(bot, update):
    '''Command /start message handler'''
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    if chat_type == "private":
        bot.send_message(chat_id, TEXT[lang]['START'])
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, TEXT[lang]['START'])


def cmd_help(bot, update):
    '''Command /help message handler'''
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    if chat_type == "private":
        bot.send_message(chat_id, TEXT[lang]['HELP'])
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, TEXT[lang]['HELP'])


def cmd_commands(bot, update):
    '''Command /commands message handler'''
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    if chat_type == "private":
        bot.send_message(chat_id, TEXT[lang]['COMMANDS'])
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, TEXT[lang]['COMMANDS'])


def cmd_language(bot, update, args):
    '''Command /language message handler'''
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    allow_command = True
    if chat_type != "private":
        is_admin = user_is_admin(bot, user_id, chat_id)
        if is_admin == False:
            allow_command = False
    if allow_command:
        if len(args) == 1:
            lang_provided = args[0]
            lang_provided = lang_provided.lower()
            if lang_provided == 'en' or lang_provided == 'es':
                if lang_provided != lang:
                    lang = lang_provided
                    save_config_property(chat_id, 'Language', lang)
                    bot_msg = TEXT[lang]['LANG_CHANGE']
                else:
                    bot_msg = TEXT[lang]['LANG_SAME']
            else:
                bot_msg = TEXT[lang]['LANG_BAD_LANG']
        else:
            bot_msg = TEXT[lang]['LANG_NOT_ARG']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    if chat_type == "private":
        bot.send_message(chat_id, bot_msg)
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_enable(bot, update):
    '''Command /enable message handler'''
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    enable = get_chat_config(chat_id, 'Enable')
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if enable:
            bot_msg = TEXT[lang]['ALREADY_ENABLE']
        else:
            enable = True
            save_config_property(chat_id, 'Enable', enable)
            bot_msg = TEXT[lang]['ENABLE']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    if chat_type == "private":
        bot.send_message(chat_id, bot_msg)
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_disable(bot, update):
    '''Command /disable message handler'''
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    enable = get_chat_config(chat_id, 'Enable')
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if enable:
            enable = False
            save_config_property(chat_id, 'Enable', enable)
            bot_msg = TEXT[lang]['DISABLE']
        else:
            bot_msg = TEXT[lang]['ALREADY_DISABLE']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    if chat_type == "private":
        bot.send_message(chat_id, bot_msg)
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_version(bot, update):
    '''Command /version message handler'''
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    bot_msg = TEXT[lang]['VERSION'].format(CONST['VERSION'])
    if chat_type == "private":
        bot.send_message(chat_id, bot_msg)
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_about(bot, update):
    '''Command /about handler'''
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    bot_msg = TEXT[lang]['ABOUT_MSG'].format(CONST['DEVELOPER'], CONST['REPOSITORY'], \
        CONST['DEV_PAYPAL'], CONST['DEV_BTC'])
    if chat_type == "private":
        bot.send_message(chat_id, bot_msg)
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_know(bot, update, args):
    '''/know command handler'''
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    enable = get_chat_config(chat_id, 'Enable')
    lang = get_chat_config(chat_id, 'Language')
    wiki_lang = lang
    if enable:
        search_for = ""
        if len(args) > 0:
            first_term = True
            for arg in args:
                if not first_term:
                    search_for = "{} {}".format(search_for, arg)
                else:
                    if arg[0] == '-':
                        if arg[1:] in CONST['ISO_LANG_CODES']:
                            wiki_lang = arg[1:]
                        else:
                            search_for = arg
                            first_term = False
                    else:
                        search_for = arg
                        first_term = False
            wikipedia.set_lang(wiki_lang)
            try:
                wiki = wikipedia.page(search_for)
                search_for_hlink = "<a href=\"{}\">{}</a>".format(wiki.url, wiki.title)
                summary_short = "{}.".format(wiki.summary.partition('.')[0])
                bot_response = TEXT[lang]['KNOW_RESPONSE'].format(search_for_hlink, summary_short)
            except Exception as e:
                bot_response = TEXT[lang]['KNOW_RESPONSE'].format(search_for, 
                               TEXT[lang]['KNOW_RESPONSE_NO_INFO'])
            bot.send_message(chat_id, bot_response, parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id, TEXT[lang]['KNOW_RESPONSE_NO_ARG'])


def cmd_knowall(bot, update, args):
    '''/knowall command handler'''
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    enable = get_chat_config(chat_id, 'Enable')
    lang = get_chat_config(chat_id, 'Language')
    wiki_lang = lang
    if enable:
        search_for = ""
        if len(args) > 0:
            first_term = True
            for arg in args:
                if not first_term:
                    search_for = "{} {}".format(search_for, arg)
                else:
                    if arg[0] == '-':
                        if arg[1:] in CONST['ISO_LANG_CODES']:
                            wiki_lang = arg[1:]
                        else:
                            search_for = arg
                            first_term = False
                    else:
                        search_for = arg
                        first_term = False
            wikipedia.set_lang(wiki_lang)
            try:
                wiki = wikipedia.page(search_for)
                search_for_hlink = "<a href=\"{}\">{}</a>".format(wiki.url, wiki.title)
                bot_response = TEXT[lang]['KNOW_RESPONSE'].format(search_for_hlink, wiki.summary)
            except Exception as e:
                bot_response = TEXT[lang]['KNOW_RESPONSE'].format(search_for, 
                               TEXT[lang]['KNOW_RESPONSE_NO_INFO'])
            bot.send_message(chat_id, bot_response, parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id, TEXT[lang]['KNOW_ALL_RESPONSE_NO_ARG'])

####################################################################################################

def inlinequery(bot, update):
    """Handle the inline query"""
    chat_id = update.inline_query.id
    all_summary = False
    lang = "en"
    wiki_lang = lang
    results = []
    results.clear()
    query = update.inline_query.query
    query_words = query.split(' ')
    if len(query_words) > 1:
        # Check if first word is for all summary search
        if(query_words[0] == "-all"):
            all_summary = True
            if query_words[1][0] == '-':
                if query_words[1][1:] in CONST['ISO_LANG_CODES']:
                    wiki_lang = query_words[1][1:]
                    query = query[9:]
                else:
                    if query_words[0][0] == '-':
                        article_result = InlineQueryResultArticle(
                            id=uuid4(),
                            title="Invalid or not supported language",
                            input_message_content=InputTextMessageContent(
                                "Invalid or not supported language"
                            )
                        )
                        results.append(article_result)
                        update.inline_query.answer(results)
                        query = ""
                    else:
                        query = query[5:]
        else:
            # Check if first word is for language search ("/en", "/es")
            if query_words[0][0] == '-':
                if query_words[0][1:] in CONST['ISO_LANG_CODES']:
                    wiki_lang = query_words[0][1:]
                    if(query_words[1] == "-all"):
                        all_summary = True
                        query = query[9:]
                    else:
                        query = query[4:]
                else:
                    if query_words[0][0] == '-':
                        article_result = InlineQueryResultArticle(
                            id=uuid4(),
                            title="Invalid or not supported language",
                            input_message_content=InputTextMessageContent(
                                "Invalid or not supported language"
                            )
                        )
                        results.append(article_result)
                        update.inline_query.answer(results)
                        query = ""
    if query:
        try:
            wikipedia.set_lang(wiki_lang)
            wiki_search = wikipedia.search(query, results=3)
            for search_result in wiki_search:
                wiki = wikipedia.page(search_result)
                result_hlink = "<a href=\"{}\">{}</a>".format(wiki.url, wiki.title)
                if all_summary:
                    result_summary_short = wiki.summary
                else:
                    result_summary_short = "{}.".format(wiki.summary.partition('.')[0])
                response = TEXT[lang]['KNOW_RESPONSE'].format(result_hlink, result_summary_short)
                article_result = InlineQueryResultArticle(
                    id=uuid4(),
                    title=wiki.title,
                    thumb_url=wiki.url,
                    description=result_summary_short,
                    input_message_content=InputTextMessageContent(response, ParseMode.HTML)
                )
                results.append(article_result)
        except Exception as e:
            response = TEXT[lang]['KNOW_RESPONSE_NO_INFO']
            article_result = InlineQueryResultArticle(
                id=uuid4(),
                title=query,
                description=response,
                input_message_content=InputTextMessageContent(response, ParseMode.HTML)
            )
            results.append(article_result)
        if results:
            update.inline_query.answer(results)

####################################################################################################

### Main function ###
def main():
    ''' Main Function'''
    # Initialize resources by populating files list and configs with chats found files
    initialize_resources()
    # Create an event handler (updater) for a Bot with the given Token and get the dispatcher
    updater = Updater(CONST['TOKEN'])
    dp = updater.dispatcher
    # Set the received commands handlers into the dispatcher
    dp.add_handler(CommandHandler("start", cmd_start))
    dp.add_handler(CommandHandler("help", cmd_help))
    dp.add_handler(CommandHandler("commands", cmd_commands))
    dp.add_handler(CommandHandler("language", cmd_language, pass_args=True))
    dp.add_handler(CommandHandler("enable", cmd_enable))
    dp.add_handler(CommandHandler("disable", cmd_disable))
    dp.add_handler(CommandHandler("know", cmd_know, pass_args=True))
    dp.add_handler(CommandHandler("knowall", cmd_knowall, pass_args=True))
    dp.add_handler(CommandHandler("version", cmd_version))
    dp.add_handler(CommandHandler("about", cmd_about))
    # Set the Inline request handler into the dispatcher
    dp.add_handler(InlineQueryHandler(inlinequery))
    # Start the Bot polling ignoring pending messages (clean=True)
    updater.start_polling(clean=True)
    # Handle self-messages delete
    selfdestruct_messages(updater.bot)

####################################################################################################

### Execute the main function if the file is not an imported module ###
if __name__ == '__main__':
    main()

### End Of Code ###