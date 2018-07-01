# -*- coding: utf-8 -*-
'''
Script:
    Knowthatbot.py
Description:
    Constants values for knowthatbot.py.
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

### Constants ###
CONST = {
    'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', # Bot Token (get it from @BotFather)
    'DATA_DIR' : './data', # Data directory path
    'F_CONF' : 'configs.json', # Chat configurations JSON files name
    'INIT_LANG' : 'en', # Initial language at Bot start
    'INIT_ENABLE' : True, # Initial enable/disable status at Bot start
    'T_DEL_MSG' : 5, # Time (in mins) to remove self-destruct sent messages from the Bot
    'DEVELOPER' : '@JoseTLG', # Bot developer
    'REPOSITORY' : 'https://github.com/J-Rios/TLG_TheKnowThatBot', # Bot code repository
    'DEV_PAYPAL' : 'https://www.paypal.me/josrios', # Developer Paypal address
    'DEV_BTC' : '3N9wf3FunR6YNXonquBeWammaBZVzTXTyR', # Developer Bitcoin address
    'VERSION' : '1.1.0', # Bot version
    'ISO_LANG_CODES' : ['en', 'es', 'de', 'fr', 'it', 'pt', 'ru', 'hi', 'ja', 'zh'] # ISO lang codes
}

TEXT = {
    'en' : {
        'START' : \
            'I am a Bot that know everything (ok, just kidding, but I know a lot). You can ' \
            'request some of my acknoledge from anything through an Inline request or using the ' \
            'command /know (or knowall), and I will response you with a short and accurate ' \
            'answer about that stuff. Check /help command for information about how I work.',

        'HELP' : \
            'Bot help:\n' \
            '————————————————\n' \
            '- How I really work? When you request some info, I search and response with the ' \
            'most fiable Wikipedia results of that stuff.\n' \
            '\n' \
            '- You can talk to me in private, add me to some group, or send me an inline ' \
            'request from anywhere.\n' \
            '\n' \
            '- You can request a short info with the command /know following with a ' \
            'topic/stuff. If you want a more complete info response, use the command /knowall.\n' \
            'Example:\n/know telegram\n/knowall telegram\n' \
            '\n' \
            '- You can change the language that I speak in a chat (Wikipedia searchs responses ' \
            'language), using the command /language.\n' \
            '\n' \
            '- You can enable or disable my functionality using /enable and /disable commands.\n' \
            '\n' \
            '- Language configuration and enable/disable commands just can be used in groups ' \
            'and just from Administrators.\n' \
            '\n' \
            '- You can request some info through an Inline request, just type my alias following ' \
            'the topic/stuff that you want to know.\n' \
            '\n' \
            '- You can request a long response and/or specify language in Inline queries, using ' \
            'the -all and -language_code (-en, -es, -fr, -it...) flags before the topic/stuff to ' \
            'know.\n' \
            'Example:\n@tknowbot -all -es telegram\n@tknowbot -all -en telegram\n'
            '\n' \
            '- To preserve a clean group, I auto-remove messages related to me, after {} minutes ' \
            '(except /know commands and knowledge responses).\n' \
            '\n' \
            '- Check /commands for get a list of all avaliable commands, and a short ' \
            'description of all of them.',

        'CMD_NOT_ALLOW' : \
            'Just an Admin can use this command',

        'LANG_CHANGE' : \
            'Language changed to english.',

        'LANG_SAME' : \
            'I am already in english.\n\nMay you want to say:\n/language es',

        'LANG_BAD_LANG' : \
            'Invalid language provided. The actual languages supported are english and spanish, ' \
            'change any of them using "en" or "es".\n' \
            '\n' \
            'Example:\n' \
            '/language en\n' \
            '/language es',

        'LANG_NOT_ARG' : \
            'The command needs a language to set (en - english, es - spanish).\n' \
            '\n' \
            'Example:\n' \
            '/language en\n' \
            '/language es',

        'ENABLE' : \
            'Bot /know requests enabled. Disable it with /disable command.',

        'DISABLE' : \
            'Bot /know requests  disabled. Enable it with /enable command.',

        'ALREADY_ENABLE' : \
            'I am already enabled.',

        'ALREADY_DISABLE' : \
            'I am already disabled.',

        'CAN_NOT_GET_ADMINS' : \
            'Can\'t use this command in the current chat.',

        'VERSION' : \
            'Actual Bot version: {}',

        'ABOUT_MSG' : \
            'This is an open-source GNU-GPL licensed Bot developed by the telegram user {}. You ' \
            'can check the code here:\n{}\n\n-----------------------------------------------\n\n' \
            'Do you like my work? Buy me a coffee.\n\nPaypal:\n{}\n\nBTC:\n{}',

        'KNOW_RESPONSE' : \
            '{}\n————————————————\n{}',

        'KNOW_RESPONSE_NO_INFO' : \
            'No information found for that...',

        'KNOW_RESPONSE_NO_ARG' : \
            'You need to specify something.\nExample:\n/know telegram',

        'KNOW_ALL_RESPONSE_NO_ARG' : \
            'You need to specify something.\nExample:\n/knowall telegram',

        'LINE' : \
            '\n————————————————\n',

        'LINE_LONG' : \
            '\n————————————————————————————————————————————————\n',

        'COMMANDS' : \
            'List of commands:\n' \
            '————————————————\n' \
            '/start - Show the initial information about the bot.\n' \
            '\n' \
            '/help - Show the help information.\n' \
            '\n' \
            '/commands - Show the actual message. Information about all the available commands ' \
            'and their description.\n' \
            '\n' \
            '/language - Allow to change the language of the bot messages. Actual available ' \
            'languages: en (english) - es (spanish).\n' \
            '\n' \
            '/enable - Enable the functionality.\n' \
            '\n' \
            '/disable - Disable the functionality.\n' \
            '\n' \
            '/know - Ask for information about anything (short response).\n' \
            '\n' \
            '/knowall - Ask for information about anything (complete response).\n' \
            '\n' \
            '/version - Show the version of the Bot.\n' \
            '\n' \
            '/about - Show about info.'
    },
    'es' : {
        'START' : \
            'Soy un Bot que lo sabe absolutamente todo (esta bien, es broma, pero sí que se un ' \
            'monton de cosas). Puedes pedirme un poco de conocimiento respecto a algo usando el ' \
            'comando /know y te daré una respuesta corta y precisa sobre esa cosa. Echa un ' \
            'vistazo al comando /help para conocer más información sobre mi uso.',

        'HELP' : \
            'Ayuda sobre el Bot:\n' \
            '————————————————\n' \
            '- Cómo funciono realmente? Cuando me pides alguna información, busco en Wikipedia ' \
            'sobre ello y te respondo con el resultado más fiable obtenido.\n' \
            '\n' \
            '- Puedes pedirme algo de mi conocimiento mediante el comando /know seguido de ' \
            'alguna cosa.\n'
            'Ejemplo: /know telegram\n' \
            '\n' \
            '- Puedes configurar el idioma en el que hablo (y las respuestas de busqueda de ' \
            ' Wikipedia) mediante el comando /language.\n' \
            '\n' \
            '- Puedes activar/desactivar mi funcionalidad con los comandos /enable y /disable.\n' \
            '\n' \
            '- Los comandos de configuración de idioma y activación/desactivación solo pueden ' \
            'ser utilizados por los Administradores del grupo.\n' \
            '\n' \
            '- Para mantener limpio el grupo, elimino aquellos mensajes que tengan relación ' \
            'conmigo, pasados {} minutos (salvo mensajes de /know y sus repuestas).\n' \
            '\n' \
            '- Echa un vistazo al comando /commands para ver una lista con todos los comandos ' \
            'disponibles y una breve descripción de cada uno de ellos.\n',

        'CMD_NOT_ALLOW' : \
            'Solo un Admin puede utilizar este comando.',

        'LANG_CHANGE' : \
            'Idioma cambiado a español.',

        'LANG_SAME' : \
            'Ya estoy en español.\n\nQuizás querías decir:\n/language en',

        'LANG_BAD_LANG' : \
            'Idioma inválidado. Los idiomas actualmente soportados son el español y el inglés, ' \
            'cambia a uno de ellos mediante las etiquetas "es" o "en".\n' \
            '\n' \
            'Ejemplo:\n' \
            '/language es\n' \
            '/language en',

        'LANG_NOT_ARG' : \
            'El comando necesita un idioma que establecer (es - español, en - inglés).\n' \
            '\n' \
            'Ejemplo:\n' \
            '/language es\n' \
            '/language en',

        'ENABLE' : \
            'Consultas /know activadas. Desactívalas con el comando /disable.',

        'DISABLE' : \
            'Consultas /know desactivadas. Actívalas con el comando /enable.',

        'ALREADY_ENABLE' : \
            'Ya estoy activado.',

        'ALREADY_DISABLE' : \
            'Ya estoy desactivado.',

        'CAN_NOT_GET_ADMINS' : \
            'No se puede usar este comando en el chat actual.',

        'VERSION' : \
            'Versión actual del Bot: {}',

        'ABOUT_MSG' : \
            'Este es un Bot open-source con licencia GNU-GPL, desarrollado por el usuario de ' \
            'telegram {}. Puedes consultar el código aquí:\n{}\n\n' \
            '-----------------------------------------------\n\nTe gusta lo que hago? ' \
            'Invítame a un café.\n\nPaypal:\n{}\n\nBTC:\n{}',

        'KNOW_RESPONSE' : \
            '{}\n————————————————\n{}',

        'KNOW_RESPONSE_NO_INFO' : \
            'No se encontró ninguna información sobre eso...',

        'KNOW_RESPONSE_NO_ARG' : \
            'Tienes que especificar algo.\nEjemplo:\n/know telegram',

        'KNOW_ALL_RESPONSE_NO_ARG' : \
            'Tienes que especificar algo.\nEjemplo:\n/knowall telegram',

        'LINE' : \
            '\n————————————————\n',

        'LINE_LONG' : \
            '\n————————————————————————————————————————————————\n',

        'COMMANDS' : \
            'Lista de comandos:\n' \
            '————————————————\n' \
            '/start - Muestra la información inicial sobre el Bot.\n' \
            '\n' \
            '/help - Muestra la información de ayuda.\n' \
            '\n' \
            '/commands - Muestra el mensaje actual. Información sobre todos los comandos ' \
            'disponibles y su descripción.\n' \
            '\n' \
            '/language - Permite cambiar el idioma en el que habla el Bot. Idiomas actualmente ' \
            'disponibles: es (español) - en (inglés).\n' \
            '\n' \
            '/enable - Activa la funcionalidad.\n' \
            '\n' \
            '/disable - Desactiva la funcionalidad.\n' \
            '\n' \
            '/know - Pide información sobre cualquier cosa (respuesta breve y concisa).\n' \
            '\n' \
            '/knowall - Pide información sobre cualquier cosa (respuesta completa).\n' \
            '\n' \
            '/version - Consulta la versión del Bot.\n' \
            '\n' \
            '/about - Muestra la información \"acerca de...\" del Bot.'
    }
}