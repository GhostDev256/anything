#by Ghost
#Гемор.

import amino, random, time, os

print("Подключаюсь...")

client = amino.Client(' ')
client.login(email=' ', password=' ')
sub_client = amino.SubClient(comId='', profile=client.profile)

badWord = open("message_badWord.txt", "r", encoding="utf-8")
badWordList = badWord.read().split(",")
badWord.close()

message_log_num = 0
message_log_max = 35

#Опции
options_anti_raid_file = open(f"Info/Options anti raid.txt", "r", encoding="utf-8")
options_anti_raid = str(options_anti_raid_file.read())
options_anti_raid_file.close()

options_chat_assistant_file = open(f"Info/Options chat assistant.txt", "r", encoding="utf-8")
options_chat_assistant = str(options_chat_assistant_file.read())
options_chat_assistant_file.close()

'''options_function_interlocutor_file = open(f"Info/Options function interlocutor.txt", "r", encoding="utf-8")
options_function_interlocutor = str(options_function_interlocutor_file.read())
options_function_interlocutor_file.close()'''

options_greeting_file = open(f"Info/Options greeting.txt", "r", encoding="utf-8")
options_greeting = str(options_greeting_file.read())
options_greeting_file.close()

options_response_mats_in_blogs_file = open(f"Info/Options response mats in blogs.txt", "r", encoding="utf-8")
options_response_mats_in_blogs = str(options_response_mats_in_blogs_file.read())
options_response_mats_in_blogs_file.close()

options_response_mats_in_chats_file = open(f"Info/Options response mats in chats.txt", "r", encoding="utf-8")
options_response_mats_in_chats = str(options_response_mats_in_chats_file.read())
options_response_mats_in_chats_file.close()

'''options_sendingGreetings_file = open(f"Info/Options sending greetings.txt", "r", encoding="utf-8")
options_sendingGreetings = str(options_sendingGreetings_file.read())
options_sendingGreetings_file.close()'''

options_specify_chat_complaints_file = open(f"Info/Options specify chat complaints.txt", "r", encoding="utf-8")
options_specify_chat_complaints = str(options_specify_chat_complaints_file.read())
options_specify_chat_complaints_file.close()

spam_message_user = ""
spam_message_back = ""
spam_message_index = 0

print("Все готово.")

def is_non_zero_file(fpath):  
    fpath.seek(0, os.SEEK_END) 
    if fpath.tell(): 
        return False
    else:        
        return True

def concat_option(OnOff):  
    if OnOff == "False": 
        return "off"
    if OnOff == "True":        
        return "on"

@client.callbacks.event("on_text_message")
def on_text_message(data):  

    root_users_file = open(f"Info/Root users.txt", "r", encoding="utf-8")
    root_users = root_users_file.read().split(",")
    root_users_file.close()

    bot_name_file = open(f"Info/Bot name.txt", "r", encoding="utf-8")
    bot_name_file = bot_name_file.read().split(" ")
    bot_name_file.append(bot_name_file[0])
    bot_name_file.append(bot_name_file[0] + ",")
    _bot_name = [""]
    for i in bot_name_file:
        _bot_name.append(i.lower())
    bot_name = _bot_name
    
    mes_time = time.strftime("Число: %d.%m.%Y (д/м/г).\nВремя: %X (по МСК).", time.localtime())

    id = data.message.messageId
    user_name = data.message.author.nickname
    _user_name = user_name.split(" ")
    user_id = data.message.author.userId
    _content = data.message.content
    chatId = data.message.chatId
    chat_name = str(sub_client.get_chat_thread(data.message.chatId).title)

    global message_log_num, message_log_max
    if _user_name[0].lower() not in (bot_name):
        message_log_num += 1
        message_log = open(f"Logs/log_{message_log_num}.txt", "w", encoding="utf-8")
        message_log.write(f"{mes_time}\nИмя чата: '{chat_name}'.\nid чата: '{chatId}'.\nИмя пользователя: '{user_name}'.\nid пользователя: '{user_id}'.\n\nСообщение: '{_content}'.")
        message_log.close()
        if message_log_num == message_log_max:
            message_log_num = 0

    #В терминал
    print(f"----------------------------------------------") 
    print(f"{mes_time}")
    print(f"Имя чата: {chat_name}, id чата: {chatId}.")
    print(f"Имя пользователя: {user_name}, id пользователя: {user_id}.")
    print(f" ")
    print(f"Сообщение: {_content}")
    
    contents = str(data.message.content).split(" ")
    contents_no_comma = str(data.message.content).split(",") 
    contents_no_slash = str(data.message.content).split("/")
    contents_no_questionMark = str(data.message.content).split("!")
    contents_no_exclamationPoint = str(data.message.content).split("?")
    contents_no_point = str(data.message.content).split(".")
    content = contents_no_comma + contents + contents_no_point + contents_no_slash + contents_no_questionMark + contents_no_exclamationPoint
    content = set(content)

    global spam_message_index, spam_message_back, spam_message_user
    spam_message_index += 1
    if spam_message_index == 2:
        if spam_message_back == _content and (spam_message_user == user_name and spam_message_user not in bot_name):
            spam_message_index = 1
            
            sub_client.send_message(chatId=chatId, message="Давайте не спамить, окей?", replyTo=id)           
            
            message_complaint = f"Участник '{user_name}' спамит в чате '{chat_name}'.\n\n{mes_time}.\n\nСообщение: '{_content}' было отправлено более трех раз подряд."                                                               
            sub_client.send_message(chatId=options_specify_chat_complaints, message=message_complaint)

            #Костыли мои костыли...
            if options_chat_assistant == "True":
                try:
                    sub_client.kick(chatId=chatId, userId=user_id)
                except BaseException:
                    pass

        else:
            spam_message_back = _content
            spam_message_user = user_name
            spam_message_index = 0

    for i in content:
        if i.lower() in (badWordList) and _user_name[0].lower() not in (bot_name) and chat_name != "None" and options_response_mats_in_chats == "True":
            message_warning = ["Попался.", f"{user_name}, а я все вижу!", 
                                "Ой, что я вижу?", 
                                "А так не надо, пожалуйста.", 
                                f"Жить надоело, {user_name}?", "Вообще-то, я еще тут.",
                                "Press F."]
            sub_client.send_message(chatId=chatId, message=random.choice(message_warning), replyTo=id)            
            
            message_complaint = f"Участник '{user_name}' нарушил правила в чате '{chat_name}'.\n\n{mes_time}.\n\nЦитирую: '{_content}'."                                                               
            sub_client.send_message(chatId=options_specify_chat_complaints, message=message_complaint) #"fa9b3477-6e83-4b01-8623-0705cf77e774"

            if options_chat_assistant == "True":
                try:
                    sub_client.kick(chatId=chatId, userId=user_id)
                except BaseException:
                    pass

    '''massege_greeting = ["привет", "привет.", "привет!", "привет?", 
                        "хеллоу", "хеллоу.", "хеллоу!", "хеллоу?",
                        "хелоу", "хелоу.", "хелоу!", "хелоу?",
                        "хай", "хай.", "хай!", "хай?"
                        "хой", "хой.", "хой!",
                        "hi", "hi.", "hi!", "hi?",
                        "hai", "hai.", "hai!", "hai?",
                        "hoi", "hoi.", "hoi!", "hoi?",
                        "hello", "hello.", "hello!", "hello?",
                        "helo", "helo.", "helo!", "helo?",
                        "хац", "хац.", "хац!",
                        "приветствую", "приветствую.", "приветствую!", "приветствую?",
                        "здравствуйте", "здраствуйте.", "здраствуйте!", "здраствуйте?",
                        "привит", "привит.", "привит!", "привит?",
                        "привки", "привки.", "привки!", "привки?",
                        "прив", "прив.", "прив!", "прив?",
                        "здрасте", "здрасте.", "здрасте!", "здрасте?",
                        "драсте", "драсте.", "драсте!", "драсте?",
                        "приветик", "приветик.", "приветик!", "приветик?"]
    for i in contents:
        if (i.lower() in massege_greeting) and (_user_name[0].lower() not in bot_name) and (options_greeting == "True"):        
            massege_hiList = [f"Привет, {user_name}!", f"Приветик, {user_name}.", "Хай. 👀", "Привет!", f"Здраствуй, {user_name}!"]
            sub_client.send_message(chatId=chatId, message=random.choice(massege_hiList), replyTo=id)'''

    if contents[0][0:].lower() in (bot_name):
        if contents[1][0:].lower() in ("commands", "commands.", "commands?"):
            message_help = open("message_help.txt", "r", encoding="utf-8")
            sub_client.send_message(chatId=chatId, message=message_help.read(), replyTo=id)
            message_help.close()

        if contents[1][0:].lower() in ("alive", "alive?", "alive."):
            message_alive = ["Конечно. 👀", "Угу.", f"Да куда я денусь, {user_name}? 👀", "Да.", "А как же?", "👀"]
            sub_client.send_message(chatId=chatId, message=random.choice(message_alive), replyTo=id)

        if contents[1][0:].lower() in ("do_the_magic", "do_the_magic."):
            sub_client.send_message(chatId=chatId, message="Магия.", messageType=100)

        if contents[1][0:].lower() in ("tell_me_joke", "tell_me_joke", "tell_me_joke."):
            sub_client.send_message(chatId=chatId, message="Окей, секунду.", replyTo=id)
            joke_num = "Anecdotes/1 — копия (" + str(random.randint(1, 100)) + ").txt"
            message_joke = open(joke_num, "r", encoding="utf-8")
            sub_client.send_message(chatId=chatId, message=message_joke.read())
            message_joke.close()

        #Команды для рут-пользователей.
        #Вывести айди текущего чата. 
        if contents[1][0:].lower() in ("get_chatid", "get_chatid.") and user_id in root_users:
            sub_client.send_message(chatId=chatId, message=chatId, replyTo=id)
        if contents[1][0:].lower() in ("get_chatid", "get_chatid.") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Вывести список рут-команд
        if contents[1][0:].lower() in ("root_commands", "root_commands.") and user_id in root_users:
            message_root_commands = open("message_root_commands.txt", "r", encoding="utf-8")
            sub_client.send_message(chatId=chatId, message=message_root_commands.read(), replyTo=id)
            message_root_commands.close()
        if contents[1][0:].lower() in ("root_commands", "root_commands.") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Дать рут-права.
        if contents[1][0:].lower() == "give_root" and user_id in root_users:
            if contents[2] in root_users:
                sub_client.send_message(chatId=chatId, message="Такой уже есть.", replyTo=id)
            else:
                sub_client.send_message(chatId=chatId, message=f"Принято, {user_name}.", replyTo=id)

                root_users_file = open(f"Info/Root users.txt", "a", encoding="utf-8")
                root_users_file.write(f",{contents[2]}")
                root_users_file.close()

        if contents[1][0:].lower() == "give_root" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Отобрать рут-права. 
        if contents[1][0:].lower() == "select_root" and user_id in root_users:
            if contents[2] != "8d39d89a-3db9-438e-a740-28574cd68268":
                sub_client.send_message(chatId=chatId, message=f'Такого нету в списке, {user_name}. 👀"', replyTo=id)
                if contents[2] not in root_users:
                    sub_client.send_message(chatId=chatId, message=f'Такого нету в списке, {user_name}. 👀"', replyTo=id)
                else:
                    for i in root_users:
                        if i in contents[2]:
                            root_users.remove(i)
                            root_users_file = open(f"Info/Root users.txt", "w", encoding="utf-8")
                            root_users_file.write("")
                            root_users_file.close()
                            for r in root_users:
                                root_users_file = open(f"Info/Root users.txt", "a", encoding="utf-8")
                                root_users_file.write("," + r)
                                root_users_file.close()
            else:
                sub_client.send_message(chatId=chatId, message=f"Не, ты не можешь отобрать рут у этого пользователя.", replyTo=id)
        
                sub_client.send_message(chatId=chatId, message=f"Сделано.", replyTo=id)
        if contents[1][0:].lower() == "select_root" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Вывести список рут-пользователей.
        if contents[1][0:].lower() in ("root_users_list", "root_users_list.", "root_users_list!") and user_id in root_users:
            sub_client.send_message(chatId=chatId, message="Окей, сейчас.", replyTo=id)     
            root_users_index = -1
            root_users_message = "[C]Список рут-пользователей.\n"
            for i in root_users:
                root_users_index += 1
                if root_users_index >= 1:
                    root_users_message += f"[C]{root_users_index}.\nНикнейм: '{sub_client.get_user_info(i).nickname}'.\nАйди: '{i}'.\n"
                else:
                    root_users_message += "\n"
            sub_client.send_message(chatId=chatId, message=root_users_message)
        if contents[1][0:].lower() in ("root_users_list", "root_users_list.", "root_users_list!") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Присоединиться к чату.
        #С указанием Айди
        if contents[1][0:].lower() in ("join_the_chat") and user_id in root_users: 
            sub_client.send_message(chatId=chatId, message="Окей, минутку...", replyTo=id)     
            sub_client.join_chat(chatId=contents[2])       
        if contents[1][0:].lower() in ("join_the_chat") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Без указания Айди.
        if contents[1][0:].lower() in ("join_the_chat.") and user_id in root_users: 
            sub_client.join_chat(chatId=chatId)        
        if contents[1][0:].lower() in ("join_the_chat.") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Выйти из чата.     
        #С указанием Айди.
        if contents[1][0:].lower() in ("leave_the_chat") and user_id in root_users: 
            sub_client.send_message(chatId=chatId, message="Ладно...", replyTo=id)     
            sub_client.leave_chat(chatId=contents[2])      
        if contents[1][0:].lower() in ("leave_the_chat") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Без указания Айди.
        if contents[1][0:].lower() in ("leave_the_chat.") and user_id in root_users: 
            sub_client.send_message(chatId=chatId, message="Ладно...", replyTo=id)     
            sub_client.leave_chat(chatId=chatId)      
        if contents[1][0:].lower() in ("leave_the_chat.") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Подписаться на пользователя. 
        if contents[1][0:].lower() == "subscribe" and user_id in root_users: 
            sub_client.send_message(chatId=chatId, message="Окей, сейчас.", replyTo=id)      
            sub_client.follow(userId=contents[2])
        if contents[1][0:].lower() == "subscribe" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Отписаться от пользователя. 
        if contents[1][0:].lower() == "unsubscribe" and user_id in root_users: 
            sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)    
            sub_client.unfollow(userId=contents[2])       
        if contents[1][0:].lower() == "unsubscribe" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Вывести список чатов, в которых находиться учетная записть бота (в пределах текущего сообщества). 
        if contents[1][0:].lower() in ("get_chat_list", "get_chat_list.") and user_id in root_users: 
            sub_client.send_message(chatId=chatId, message="Окей, сейчас.", replyTo=id)       
            chat_list = sub_client.get_chat_threads().title
            chat_list_id = sub_client.get_chat_threads().chatId
            
            index_chat, index_chat_id = 0, 0
            for i in chat_list:
                if i == None:
                    index_chat_id -= 1
                    continue
                index_chat += 1     
                index_chat_id += 1  
                sub_client.send_message(chatId=chatId, message=f"[IC]{index_chat}.\n\nИмя чата: '{i}'.\n\nЕго id: {chat_list_id[index_chat_id]}.")                         
            sub_client.send_message(chatId=chatId, message="Это все.")
        if contents[1][0:].lower() in ("get_chat_list", "get_chat_list.") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)
        
        #Включить/выключить приветствие участников в чате. 
        if contents[1][0:].lower() == "greeting" and user_id in root_users: 
            if contents[2].lower() in ("on", "on.", "on!") and options_greeting != "True":
                options_greeting_file = open(f"Info/Options greeting.txt", "w", encoding="utf-8")
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)  
                options_greeting_file.write("True")
                options_greeting_file.close()
            if contents[2].lower() in ("on", "on.", "on!") and options_greeting == "True":
                sub_client.send_message(chatId=chatId, message=f"Приветствия участников уже включены.", replyTo=id)

            if contents[2].lower() in ("off", "off.", "off!") and options_greeting != "False":
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)                  
                options_greeting_file = open(f"Info/Options greeting.txt", "w", encoding="utf-8")
                options_greeting_file.write("False")
                options_greeting_file.close()
            if contents[2].lower() in ("off", "off.", "off!") and options_greeting == "False":
                sub_client.send_message(chatId=chatId, message=f"Приветствия участников и так выключены.", replyTo=id)
  
        if contents[1][0:].lower() == "greeting" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Включить/выключить вылавливание матов/ругательств из чатов. 
        if contents[1][0:].lower() == "response_mats_in_chats" and user_id in root_users: 
            if contents[2].lower() in ("on", "on.", "on!") and options_response_mats_in_chats != "True":
                options_response_mats_in_chats_file = open(f"Info/Options response mats in chats.txt", "w", encoding="utf-8")
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)  
                options_response_mats_in_chats_file.write("True")
                options_response_mats_in_chats_file.close()
            if contents[2].lower() in ("on", "on.", "on!") and options_response_mats_in_chats == "True":
                sub_client.send_message(chatId=chatId, message=f"Реагирование на маты в чатах уже включено.", replyTo=id)

            if contents[2].lower() in ("off", "off.", "off!") and options_response_mats_in_chats != "False":
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)                  
                options_response_mats_in_chats_file = open(f"Info/Options response mats in chats.txt", "w", encoding="utf-8")
                options_response_mats_in_chats_file.write("False")
                options_response_mats_in_chats_file.close()
            if contents[2].lower() in ("off", "off.", "off!") and options_response_mats_in_chats == "False":
                sub_client.send_message(chatId=chatId, message=f"Реагирование на маты в чатах и так выключено.", replyTo=id)

        if contents[1][0:].lower() == "response_mats_in_chats" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        '''#Включить/выключить вылавливание матов/ругательств из блогов. 
        if contents[1][0:].lower() == "response_mats_in_blogs" and user_id in root_users: 
            if contents[2].lower() in ("on", "on.", "on!") and options_response_mats_in_blogs != "True":
                options_response_mats_in_blogs_file = open(f"Info/Options response mats in blogs.txt", "w", encoding="utf-8")
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)  
                options_response_mats_in_blogs_file.write("True")
                options_response_mats_in_blogs_file.close()
            if contents[2].lower() in ("on", "on.", "on!") and options_response_mats_in_blogs == "True":
                sub_client.send_message(chatId=chatId, message=f"Уже включено.", replyTo=id)

            if contents[2].lower() in ("off", "off.", "off!") and options_response_mats_in_blogs != "False":
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)                  
                options_response_mats_in_blogs_file = open(f"Info/Options response mats in blogs.txt", "w", encoding="utf-8")
                options_response_mats_in_blogs_file.write("False")
                options_response_mats_in_blogs_file.close()
            if contents[2].lower() in ("off", "off.", "off!") and options_response_mats_in_blogs == "False":
                sub_client.send_message(chatId=chatId, message=f"Оно и так выключено...", replyTo=id)

        if contents[1][0:].lower() == "response_mats_in_blogs" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)'''
        
        #Включить/выключить анти-спам. 
        if contents[1][0:].lower() == "anti_raid" and user_id in root_users: 
            if contents[2].lower() in ("on", "on.", "on!") and options_anti_raid != "True":
                options_anti_raid_file = open(f"Info/Options anti raid.txt", "w", encoding="utf-8")
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)  
                options_anti_raid_file.write("True")
                options_anti_raid_file.close()
            if contents[2].lower() in ("on", "on.", "on!") and options_anti_raid == "True":
                sub_client.send_message(chatId=chatId, message="Анти-рейд/спам-фильтр уже включен.", replyTo=id)

            if contents[2].lower() in ("off", "off.", "off!") and options_anti_raid != "False":
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)                  
                options_anti_raid_file = open(f"Info/Options anti raid.txt", "w", encoding="utf-8")
                options_anti_raid_file.write("False")
                options_anti_raid_file.close()
            if contents[2].lower() in ("off", "off.", "off!") and options_anti_raid == "False":
                sub_client.send_message(chatId=chatId, message="Анти-рейд/спам-фильтр и так выключен.", replyTo=id)

        if contents[1][0:].lower() == "anti_raid" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Включить/выключить chat_assistant. 
        if contents[1][0:].lower() == "chat_assistant" and user_id in root_users: 
            if contents[2].lower() in ("on", "on.", "on!") and options_chat_assistant != "True":
                options_chat_assistant_file = open(f"Info/Options chat assistant.txt", "w", encoding="utf-8")
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)  
                options_chat_assistant_file.write("True")
                options_chat_assistant_file.close()
            if contents[2].lower() in ("on", "on.", "on!") and options_chat_assistant == "True":
                sub_client.send_message(chatId=chatId, message=f"Опция помощника чата уже включена.", replyTo=id)

            if contents[2].lower() in ("off", "off.", "off!") and options_chat_assistant != "False":
                sub_client.send_message(chatId=chatId, message=f"Как скажешь, {user_name}.", replyTo=id)                  
                options_chat_assistant_file = open(f"Info/Options chat assistant.txt", "w", encoding="utf-8")
                options_chat_assistant_file.write("False")
                options_chat_assistant_file.close()
            if contents[2].lower() in ("off", "off.", "off!") and options_chat_assistant == "False":
                sub_client.send_message(chatId=chatId, message=f"Опция помощника чата и так выключена.", replyTo=id) 

        if contents[1][0:].lower() == "chat_assistant" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Fuck...
        #Вывести N последних сообщения из лога.
        if contents[1][0:].lower() == "get_list_log" and user_id in root_users: 
            if int(contents[2]) > 0:
                sub_client.send_message(chatId=chatId, message="Окей, готовься.", replyTo=id)

                if int(contents[2]) <= message_log_max:   
                    message_log_index = 0
                    while message_log_index <= int(contents[2]) - 1:
                        message_log_index += 1
                        message_log_conclusion = open(f"Logs/log_{message_log_index}.txt", "r", encoding="utf-8")
                        file_void = is_non_zero_file(message_log_conclusion)
                        message_log_conclusion.close()
                        if file_void:
                            message_log_conclusion = open(f"Logs/log_{message_log_index}.txt", "r", encoding="utf-8")
                            sub_client.send_message(chatId=chatId, message="По какой-то причине это сообщение не было записано.")
                            message_log_conclusion.close()
                        else:       
                            message_log_conclusion = open(f"Logs/log_{message_log_index}.txt", "r", encoding="utf-8")                 
                            sub_client.send_message(chatId=chatId, message=message_log_conclusion.read())
                            message_log_conclusion.close()
                    sub_client.send_message(chatId=chatId, message="Я все.")
                else:
                    sub_client.send_message(chatId=chatId, message=f"А, стоп. Вообще-то установленный размер лога {message_log_max}.") 
            else:
                sub_client.send_message(chatId=chatId, message=f"Это как? Не, давай нормально - больше нуля.", replyTo=id)
                  
        if contents[1][0:].lower() == "get_list_log" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Ну и гемор.
        #Вывести N сообщение из лога. 
        if contents[1][0:].lower() == "get_log" and user_id in root_users:             
            if int(contents[2]) > 0:
                sub_client.send_message(chatId=chatId, message="Один момент.", replyTo=id)

                if int(contents[2]) <= message_log_max:
                    message_log_conclusion = open(f"Logs/log_{contents[2]}.txt", "r", encoding="utf-8")
                    file_void = is_non_zero_file(message_log_conclusion)
                    message_log_conclusion.close()
                    if file_void:
                        message_log_conclusion = open(f"Logs/log_{contents[2]}.txt", "r", encoding="utf-8")
                        sub_client.send_message(chatId=chatId, message="По какой-то причине это сообщение не было записано.")
                        message_log_conclusion.close()
                    else:          
                        message_log_conclusion = open(f"Logs/log_{contents[2]}.txt", "r", encoding="utf-8")              
                        sub_client.send_message(chatId=chatId, message=message_log_conclusion.read())
                        message_log_conclusion.close()
                else: 
                    sub_client.send_message(chatId=chatId, message=f"А, стоп. Вообще-то установленный размер лога {message_log_max}.")
            else:
                sub_client.send_message(chatId=chatId, message=f"Это как? Не, давай нормально - больше нуля.", replyTo=id)

        if contents[1][0:].lower() == "get_log" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Вывести N последних сообщений из лога в определенном диапозоне.
        if contents[1][0:].lower() == "get_list_to" and user_id in root_users: 
            if int(contents[2]) > 0 and int(contents[3]) > 0 and int(contents[3]) > int(contents[2]):
                sub_client.send_message(chatId=chatId, message=f"Окей, готовься {user_name}.", replyTo=id)

                if int(contents[3]) <= message_log_max: 

                    message_log_index = int(contents[2])
                    while message_log_index <= int(contents[3]):
                        message_log_index += 1
                        message_log_conclusion = open(f"Logs/log_{message_log_index}.txt", "r", encoding="utf-8")
                        file_void = is_non_zero_file(message_log_conclusion)
                        message_log_conclusion.close()
                        if file_void:
                            message_log_conclusion = open(f"Logs/log_{message_log_index}.txt", "r", encoding="utf-8")
                            sub_client.send_message(chatId=chatId, message="По какой-то причине это сообщение не было записано.")
                            message_log_conclusion.close()
                        else:                        
                            message_log_conclusion = open(f"Logs/log_{message_log_index}.txt", "r", encoding="utf-8")
                            sub_client.send_message(chatId=chatId, message=message_log_conclusion.read())
                            message_log_conclusion.close()
                    sub_client.send_message(chatId=chatId, message="Я все.")

                else:
                    sub_client.send_message(chatId=chatId, message=f"А, стоп. Вообще-то установленный размер лога {message_log_max}.")
            else:
                sub_client.send_message(chatId=chatId, message=f"Нет, давай нормально: 0 < n1 < n2", replyTo=id)

        if contents[1][0:].lower() == "get_list_to" and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)
    
        #Установить длинну лога.
        if contents[1][0:].lower() == "list_log_max" and user_id in root_users: 
            if contents[2] in ("default", "default.", "default!"):
                sub_client.send_message(chatId=chatId, message=f"Принято.", replyTo=id)
                message_log_max = 35
                
            if int(contents[2]) < 0:
                if int(contents[2]) <= 250 and int(contents[2]) > 0:
                    sub_client.send_message(chatId=chatId, message=f"Окей, все сделано.", replyTo=id)
                    message_log_max = int(contents[2])
                else:
                    sub_client.send_message(chatId=chatId, message=f"Максимально возможное значение для установки 250.", replyTo=id)   
            else:
                sub_client.send_message(chatId=chatId, message=f"Это как? Не, давай нормально - больше нуля.", replyTo=id)             
            
        if contents[1][0:].lower() in ("list_log_max") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Показать список включенных/выключенных опций. 
        if contents[1][0:].lower() in ("get_list_options", "get_list_options.") and user_id in root_users: 
            options = f"[C]Anti_raid: {concat_option(options_anti_raid)}.\n[C]Greeting: {concat_option(options_greeting)}.\n[C]Chat assistant: {concat_option(options_chat_assistant)}.\n[C]Response mats in chats: {concat_option(options_response_mats_in_chats)}.\n[C]Response mats in blogs: {concat_option(options_response_mats_in_blogs)}.\n\n[C]Specify chat complaints:\n[C]'{str(sub_client.get_chat_thread(options_specify_chat_complaints).title)}'\n[C]{options_specify_chat_complaints}."
            sub_client.send_message(chatId=chatId, message=options, replyTo=id)      
        if contents[1][0:].lower() in ("get_list_options", "get_list_options.") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)
        
        #Указать айди чата для жалоб.
        if contents[1][0:].lower() in ("options_specify_chat_complaints") and user_id in root_users: 
            if (options_response_mats_in_chats == "True" or options_response_mats_in_blogs == "True"):

                sub_client.send_message(chatId=chatId, message="Принято.", replyTo=id)       

                options_specify_chat_complaints_file = open(f"Info/Options specify chat complaints.txt", "w", encoding="utf-8")
                options_specify_chat_complaints_file.write(str(contents[2]))
                options_specify_chat_complaints_file.close()
            else:
                sub_client.send_message(chatId=chatId, message="Функции по мониторингу чатов и/или блогов на наличие матов выключены.", replyTo=id)

        if contents[1][0:].lower() in ("options_specify_chat_complaints") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #Указать айди чата для жалоб.
        if contents[1][0:].lower() in ("options_specify_chat_complaints") and user_id in root_users: 
            if (options_response_mats_in_chats == "True" or options_response_mats_in_blogs == "True"):

                sub_client.send_message(chatId=chatId, message="Принято.", replyTo=id)       

                options_specify_chat_complaints_file = open(f"Info/Options specify chat complaints.txt", "w", encoding="utf-8")
                options_specify_chat_complaints_file.write(str(contents[2]))
                options_specify_chat_complaints_file.close()
            else:
                sub_client.send_message(chatId=chatId, message="Функции по мониторингу чатов и/или блогов на наличие матов выключены.", replyTo=id)

        if contents[1][0:].lower() in ("options_specify_chat_complaints") and user_id not in root_users:
            sub_client.send_message(chatId=chatId, message="Прости, но ты не рут-пользователь.", replyTo=id)

        #global options_greeting

    '''options_anti_raid  
    options_chat_assistant     
    options_greeting   
    options_response_mats_in_blogs     
    options_response_mats_in_chats    
    options_sendingGreetings     
    options_specify_chat_complaints''' 
    #"fa9b3477-6e83-4b01-8623-0705cf77e774"