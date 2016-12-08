from JumpScale import j

from JumpScale.clients.whmcs.WhmcsInstance import WhmcsInstance

import telebot
from telebot import types

bot = telebot.TeleBot("216671414:AAEQMTcNWwX2zGrAb6atMK7fKwhVtqt1DLE")

# info see
# https://github.com/eternnoir/pyTelegramBotAPI

#to install lib:
#pip3 install pyTelegramBotAPI

#THIS IS FOR BOT @greenitbot
#search for it to play


user_dict = {}
conversation_dict = {}

class User:
    def __init__(self, username):
        self.username = username
        self.password = None

    def __repr__(self):
        return str(self.__dict__)

class Virtualmachine:
    def __init__(self, vm_name):
        self.vm_name = vm_name
        self.cloudspace = None
        self.os = None
        self.cores = None
        self.memory = None

    def __repr__(self):
        return str(self,__dict__)       

class Docker:
    def __init__(self, docker_name):
        self.docker_name = docker_name
        self.cloud_space = None
        self.docker_host = None
        self.docker_image = None

    def __repr__(self):
        return str(self,__dict__)  

class VirtualDC:
    def __init__(self, cloud_space_name):
        self.cloud_space_name = cloud_space_name
        self.account = None


    def __repr__(self):
        return str(self,__dict__)  

class Account:
    def __init__(self, account_name):
        self.account_id = None
        self.account_name = account_name

    def __repr__(self):
        return str(self,__dict__)  

class Conversation:
    def __init__(self, id):
        self.id = id
        self.env = None
        self.location = None
        self.user = None
        self.account = None
        self.client = None
        self.cloud_space = None
        self.vm = None
        self.docker_name = None
        self.cloud_space4docker = None
        self.next = None
        self.what2lookup = None

    def __repr__(self):
        return str(self.__dict__)

@bot.message_handler(commands=['deploy'])

def process_deploy(message):
    chat_id = message.chat.id

    if chat_id in conversation_dict:
        conversation = conversation_dict[chat_id]  
    else:
        conversation = Conversation(chat_id)
        conversation_dict[chat_id] = conversation

    conversation.next = 'deploy'

    bot.reply_to(message, "So you want to deploy something...")

    ask_env(message)


def ask_env(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('du-conv-1', 'du-conv-2', 'du-conv-3', 'be-conv-2', 'be-scale-1', 'be-scale-2', 'be-scale-3', 'be-g8-1')     

        msg = bot.reply_to(message, "Please select the environment", reply_markup=markup)
        bot.register_next_step_handler(msg, process_env_selection)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_env_selection(message):
    try:
        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]
        conversation.env = message.text
        conversation.location = message.text

        if (conversation.next == 'deploy'):
            ask_username(message)
        elif (conversation.next == 'lookup port forwardings'):
            lookup_portforwardings(message)
        elif (conversation.next == 'lookup cloud spaces'):
            lookup_cloud_spaces(message)
        elif (conversation.next == 'lookup virtual machines'):
            lookup_virtual_machines(message) 
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_username(message):
    try:
        msg = bot.reply_to(message, "What is your username?")
        bot.register_next_step_handler(msg, process_username)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_username(message):
    try:
        username = message.text

        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]

        user = User(username)
        conversation.user = user

        ask_password(message)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_password(message):
    try:
        msg = bot.reply_to(message, 'Please enter your password')
        bot.register_next_step_handler(msg, process_password)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_password(message):
    try:
        password = message.text

        chat_id = message.chat.id

        conversation = conversation_dict[chat_id]

        conversation.password = password

        env = conversation.env
        url = env + '.demo.greenitglobe.com'
        username = conversation.user.username

        cl = j.clients.openvcloud.get(url, username, password)

        conversation.client = cl

        if (conversation.next == 'deploy'):
            ask_account(message)
        elif (conversation.next == 'lookup port forwardings'):
            lookup_portforwardings(message)
        elif (conversation.next == 'lookup cloud spaces'):
            lookup_cloud_spaces(message)
        elif (conversation.next == 'lookup virtual machines'):
            lookup_virtual_machines(message) 
 
    except Exception as e:
        bot.reply_to(message, 'oooops')

def ask_account(message):
    try:
        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]

        cl = conversation.client

        accounts = cl.accounts

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True) 

        for account in accounts:
            account_name = account.model['name']
            markup.add(account_name)                   

        msg = bot.reply_to(message, 'Select the account', reply_markup=markup)
        bot.register_next_step_handler(msg, process_account_selection)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_account_selection(message):
    try:
        chat_id = message.chat.id
        account_name = message.text

        conversation = conversation_dict[chat_id]

        cl = conversation.client

        account = cl.account_get(account_name)
        conversation.account = Account(account_name)
        conversation.account.account_id = account.model['id']

        if (conversation.next == 'deploy'):
            ask_what2deploy(message)
        elif (conversation.next == 'lookup port forwardings'):
            lookup_portforwardings(message)
        elif (conversation.next == 'lookup cloud spaces'):
            lookup_cloud_spaces(message)
        elif (conversation.next == 'lookup virtual machines'):
            lookup_virtual_machines(message)       

    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_what2deploy(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('vm', 'docker')

        msg = bot.reply_to(message, 'Select the resource that you want to deploy', reply_markup=markup)
        bot.register_next_step_handler(msg, process_deploy_selection)

    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_deploy_selection(message):
    try:
        resource2deploy = message.text
 
        if (resource2deploy == u'vm'):
            ask_vm_name(message)

        elif (resource2deploy == u'docker'):
            ask_docker_name(message)

        else:
            msg = bot.reply_to(message, "ERROR IN INPUT: please specify vm or docker.")
            return bot.register_next_step_handler(msg, process_deploy_step)
        
    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_vm_name(message):
    try:
        chat_id = message.chat.id

        bot.send_message(chat_id, 'Excellent, you want to deploy a virtual machine')    
        msg = bot.reply_to(message, 'What is the name of your new virtual machine?')
        return bot.register_next_step_handler(msg, process_vm_name)
        
    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_docker_name(message):
    try:
            bot.send_message(chat_id, 'Excellent, you want to deploy a docker container (NOT YET IMPLEMENTED)')    
            #msg = bot.reply_to(message, 'What is the name of your new docker container?')
            #return bot.register_next_step_handler(msg, process_docker_name)
        
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_vm_name(message):
    try:
        chat_id = message.chat.id
        vm_name = message.text
        vm = Virtualmachine(vm_name)
        conversation = conversation_dict[chat_id]
        conversation.vm = vm

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('1 core', '2 cores', '4 cores', '8 cores', '16 cores')
 
        msg = bot.reply_to(message, 'What is the number of cores that your VM needs?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_number_of_cores_selection)

    except Exception as e:
        bot.reply_to(message, "ooops")


def process_number_of_cores_selection(message):
    try:
        chat_id = message.chat.id
        cores = message.text
        conversation = conversation_dict[chat_id]
        vm = conversation.vm
        vm.cores = int(cores.split(' ')[0])

        ask_memory_size(message)

    except Exception as e:
        bot.reply_to(message, "ooops")


def ask_memory_size(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('1 GB', '2 GB', '4 GB', '8 GB', '16 GB')
 
        msg = bot.reply_to(message, 'What is the size of memory that your VM needs?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_memory_size_selection)
        
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_memory_size_selection(message):
    try:
        chat_id = message.chat.id
        memory = message.text
        conversation = conversation_dict[chat_id]
        vm = conversation.vm
        vm.memory = int(memory.split(' ')[0])

        ask_cloud_space_name(message)        

    except Exception as e:
        bot.reply_to(message, "ooooops")


def ask_cloud_space_name(message):
    try:
        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        cl = conversation.client

        account = cl.account_get(conversation.account.account_name)

        for space in account.spaces:
            space_name = space.model['name']
            markup.add(space_name)  

        msg = bot.reply_to(message, 'Select the cloud space', reply_markup=markup)
        bot.register_next_step_handler(msg, process_cloud_space_name)

    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_cloud_space_name(message):
    try:
        cloud_space_name = message.text

        chat_id = message.chat.id

        conversation = conversation_dict[chat_id]
        conversation.cloud_space = cloud_space_name
        
        if (conversation.next == 'deploy'):
            conversation.vm.cloudspace = cloud_space_name
            ask_image(message)
        elif (conversation.next == 'lookup port forwardings'):
            lookup_portforwardings(message)
        elif (conversation.next == 'lookup virtual machines'):
            lookup_virtual_machines(message) 

    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_image(message):
    try:        
        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]        
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        cl = conversation.client

        account = cl.account_get(conversation.account.account_name)

        cloud_space = account.space_get(name=conversation.vm.cloudspace, location=conversation.location, create=True)

        for image in cloud_space.images:
            image_name = image['name']
            markup.add(image_name)                   

        msg = bot.reply_to(message, 'Which operating system image do you require?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_image_selection)

    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_image_selection(message):
    try:
        image = message.text
        
        chat_id = message.chat.id
        
        conversation = conversation_dict[chat_id]
        vm = conversation.vm
        vm.os = image
        
        bot.send_message(chat_id, 'Your virtual machines will be deployed in ' + vm.cloudspace + ':\n - Virtual machine name: ' + vm.vm_name + '\n - OS Image: ' + vm.os + '\n - Number of cores: ' + str(vm.cores) + ' cores' + '\n - Memory size: ' + str(vm.memory) + ' GB')

        client = conversation.client

        account = client.account_get(conversation.account.account_name)

        cloud_space = account.space_get(vm.cloudspace, location=conversation.location, create=True)

        machine = cloud_space.machine_create(name=vm.vm_name, memsize=vm.memory, vcpus=vm.cores, disksize=10, image=vm.os)

    except Exception as e:
        bot.reply_to(message, "ooooops")


@bot.message_handler(commands=['lookup'])

def process_lookup(message):
    try:
        chat_id = message.chat.id
        if chat_id in conversation_dict:
            conversation = conversation_dict[chat_id]  
        else:
            conversation = Conversation(chat_id)
            conversation_dict[chat_id] = conversation

        bot.reply_to(message, "So you want me to lookup something...")

        conversation.what2lookup = None
        conversation.env = None
        conversation.client = None
        conversation.account = None
        conversation.cloud_space = None

        ask_what2lookup(message)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_what2lookup(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Users', 'Accounts', 'Cloud Spaces', 'Virtual Machines', 'Port Forwardings')     

        msg = bot.reply_to(message, "What to you want to lookup?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_what2lookup_selection)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_what2lookup_selection(message):
    try:

        chat_id = message.chat.id
        conversation = conversation_dict[chat_id] 

        what2lookup = message.text

        if (what2lookup == 'Port Forwardings'):
            lookup_portforwardings(message)
        elif (what2lookup == 'Cloud Spaces'):
            lookup_cloud_spaces(message)
        elif (what2lookup == 'Virtual Machines'):
            lookup_virtual_machines(message)

    except Exception as e:
        bot.reply_to(message, 'oooops')


def lookup_portforwardings(message):
    try:        
        chat_id = message.chat.id
        
        conversation = conversation_dict[chat_id]
        conversation.next = 'lookup port forwardings'

        if (conversation.env == None):
            ask_env(message)
            return
        if (conversation.client == None):
            ask_username(message)
            return
        if (conversation.account == None):
            ask_account(message)
            return
        if (conversation.cloud_space == None):
            ask_cloud_space_name(message)
            return

        client = conversation.client
        account = client.account_get(conversation.account.account_name)
        cloudspace = account.space_get(conversation.cloud_space, location=conversation.location, create=False)

        count = len(cloudspace.portforwardings)
        if (count == 0):
            response = 'No port forwardings are active for cloud space ' + conversation.cloud_space
        elif (count == 1):
            response = 'For cloud space ' + conversation.cloud_space + ' there is one port forwarding active:'
        else:
            response = 'For cloud space ' + conversation.cloud_space + ' there are ' + str(count) + ' port forwardings active:'

        for portforwarding in cloudspace.portforwardings:
            response += '\n\n ID:' + str(portforwarding['id'])
            response += '\n Protocol: ' + portforwarding['protocol']
            response += '\n Virtual Machine: ' + portforwarding['machineName'].split(' (')[0]
            #response += '\n Virtual Machine: ' + portforwarding['vmName'].split(' (')[0]
            response += '\n Private: ' + portforwarding['localIp'] + ':' + str(portforwarding['localPort'])
            response += '\n Public: ' + portforwarding['publicIp'] + ':' + str(portforwarding['publicPort'])
            
        bot.send_message(chat_id, response)

    except Exception as e:
        bot.reply_to(message, "ooooops")

def lookup_cloud_spaces(message):
    try:        
        chat_id = message.chat.id
        
        conversation = conversation_dict[chat_id]
        conversation.next = 'lookup cloud spaces'  

        if (conversation.env == None):
            ask_env(message)
            return
        if (conversation.client == None):
            ask_username(message)
            return
        if (conversation.account == None):
            ask_account(message)
            return

        client = conversation.client
        account = client.account_get(conversation.account.account_name)

        count = len(account.spaces)

        if (count == 0):
            response = 'No cloud spaces exists for the account ' + conversation.account.account_name
        elif (count == 1):
            response = 'Account ' + conversation.account.account_name + ' has one cloud space:'
        else:
            response = 'Account ' + conversation.account.account_name + ' has ' + str(count) + ' cloud spaces:'

        for cloud_space in account.spaces:
            response += '\n\n ID:' + str(cloud_space.id)
            response += '\n Name: ' + cloud_space.model['name']
            response += '\n Status: ' + cloud_space.model['status']
            response += '\n Number of Virtual Machines: ' + str(len(cloud_space.machines))
            if (cloud_space.model['status'] != 'VIRTUAL'):
                response += '\n Number of Port Forwardings: ' + str(len(cloud_space.portforwardings))
                response += '\n Public IP Address: ' + cloud_space.model['publicipaddress']

        bot.send_message(chat_id, response)

    except Exception as e:
        bot.reply_to(message, "ooooops")
        

def lookup_virtual_machines(message):
    try:        
        chat_id = message.chat.id
        
        conversation = conversation_dict[chat_id]
        conversation.next = 'lookup virtual machines'  

        if (conversation.env == None):
            ask_env(message)
            return
        if (conversation.client == None):
            ask_username(message)
            return
        if (conversation.account == None):
            ask_account(message)
            return
        if (conversation.cloud_space == None):
            ask_cloud_space_name(message)
            return

        client = conversation.client
        account = client.account_get(conversation.account.account_name)
        cloud_space = account.space_get(conversation.cloud_space, location=conversation.location, create=False)

        count = len(cloud_space.machines)

        if (count == 0):
            response = 'No virtual machines exist in cloud space ' + conversation.cloud_space
        elif (count == 1):
            response = 'Cloud space ' + conversation.account.account_name + ' has one virtual machine:'
        else:
            response = 'Cloud space ' + conversation.cloud_space + ' has ' + str(count) + ' virtual machines:'

        for machine in cloud_space.machines:
            #response += '\n\n ID:' + str(machine.id)
            response += '\n Name: ' + machine
            #response += '\n Status: ' + cloud_space.model['status']
            #response += '\n Number of Virtual Machines: ' + str(len(cloud_space.machines))

        bot.send_message(chat_id, response)

    except Exception as e:
        bot.reply_to(message, "ooooops")


@bot.message_handler(commands=['login'])

def process_login(message):
    try:
        chat_id = message.chat.id
    
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['reset'])

def process_reset(message):
    try:
        chat_id = message.chat.id
        conversation = Conversation(chat_id)
        # @todo need to find out how to remove item

    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['whmcs'])

def process_whmcs(message):
    chat_id = message.chat.id

    if chat_id in conversation_dict:
        conversation = conversation_dict[chat_id]  
    else:
        conversation = Conversation(chat_id)
        conversation_dict[chat_id] = conversation

    conversation.next = 'whmcs'

    bot.reply_to(message, "So you want to manage to WHMCS...")

    ask_what2manage_in_whmcs(message)


def ask_what2manage_in_whmcs(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Customers', 'Orders', 'Products')    

        msg = bot.reply_to(message, "Please select what you want to manage", reply_markup=markup)
        bot.register_next_step_handler(msg, process_what_2manage_in_whmcs)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_what_2manage_in_whmcs(message):
    try:
        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]

        what_2manage = message.text

        if (what_2manage == 'Customers'):
            ask_customers(message)
        elif (what_2manage == 'Orders'):
            ask_orders(message)
        elif (what_2manage == 'Products'):
            ask_products(message)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def ask_customers(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('List', 'Lookup')    

        msg = bot.reply_to(message, "Please select one of the customer actions", reply_markup=markup)
        bot.register_next_step_handler(msg, process_customer_action)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_customer_action(message):
    try:
        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]

        customer_action = message.text

        if (customer_action == 'List'):
            list_customers(message)
        elif (customer_action == 'Lookup'):
            lookup_customer(message)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def list_customers(message):
    try:
        chat_id = message.chat.id

        whmcsInstance = WhmcsInstance(username='apiadmin', md5_password='1dd1e8e488d51db56758cb78fa57632e', accesskey='jan', url='http://dev.whmcs.greenitglobe.com:7180/whmcs/includes/api.php', cloudspace_product_id='', operations_user_id = '', operations_department_id='', instance='main')

        whmcsUsers = whmcsInstance.users.list_users()

        response = ""

        for first_name, customer in whmcsUsers.items():
            response += '\n\n ID:' + customer["id"]
            response += '\nFirst Name: ' + customer["firstname"]
            response += '\nLast Name: ' + customer["lastname"]
            response += '\nCompany: ' + customer["companyname"]
            response += '\nStatus: ' + customer["status"]
            response += '\nCreated: ' + customer["datecreated"]
            response += '\nEmail: ' + customer["email"]

        bot.send_message(chat_id, response)


    except Exception as e:
        bot.reply_to(message, 'oooops')


def lookup_customer(message):
    try:
        chat_id = message.chat.id

    except Exception as e:
        bot.reply_to(message, 'oooops')

def ask_products(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('List', 'Lookup')    

        msg = bot.reply_to(message, "Please select one of the products actions", reply_markup=markup)
        bot.register_next_step_handler(msg, process_products_action)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_products_action(message):
    try:
        chat_id = message.chat.id
        conversation = conversation_dict[chat_id]

        customer_action = message.text

        if (customer_action == 'List'):
            list_products(message)
        elif (customer_action == 'Lookup'):
            lookup_product(message)
 
    except Exception as e:
        bot.reply_to(message, 'oooops')


def list_products(message):
    try:
        chat_id = message.chat.id

        whmcsInstance = WhmcsInstance(username='apiadmin', md5_password='1dd1e8e488d51db56758cb78fa57632e', accesskey='jan', url='http://dev.whmcs.greenitglobe.com:7180/whmcs/includes/api.php', cloudspace_product_id='', operations_user_id = '', operations_department_id='', instance='main')

        #import ipdb
        #ipdb.set_trace()

        whmcsProducts = whmcsInstance.products.list_products()

        response = ""

        for pid, product in whmcsProducts.items():
            response += '\n\n ID:' + product["pid"]
            response += '\nGID: ' + product["gid"]
            response += '\nName: ' + product["name"]
            #response += '\nCompany: ' + customer["companyname"]
            #response += '\nStatus: ' + customer["status"]
            #response += '\nCreated: ' + customer["datecreated"]
            #response += '\nEmail: ' + customer["email"]

        bot.send_message(chat_id, response)

    except Exception as e:
        bot.reply_to(message, 'oooops')


def lookup_product(message):
    try:
        chat_id = message.chat.id

    except Exception as e:
        bot.reply_to(message, 'oooops')


#DEBUG
#######################################
#@bot.message_handler(commands=['debug'])
#def process_debug(message):

 #   user=user_dict[message.chat.id]

 #   msg="DEBUG NOW debug, go to console of bot"
 #   print (msg)
 #   bot.reply_to(message,msg)

 #   from IPython import embed
 #   embed()



#MAIN
################

bot.polling()


"""
in botfather do

/setcommands

and then paste

questions - answer some questions
pic - show image
sticker - show sticker
sound - audio
location - show dubai location
debug - go into ipshell in telegram robot on server

"""
