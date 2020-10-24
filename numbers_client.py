# Client

import boto3
from time import time
from random import randint

def inputMessage():
""" takes no argument, returns a string with numbers separated by comma """
    message = ""
    while True:
        i = input ("number(s) {} <- ".format(message))
        # If the client stop entering numbers, the message is complete.
        if i == "":
            break
        # Adds commas between integers in message
        else:
            if len(message) > 0 and message[-1] != ",":
                message += ","
            message += i    
    return message


def sendMessage(message):
""" takes a string as argument, returns nothing, allows the client to send messages to the server """
    # initiates a connection
    sqs = boto3.resource('sqs')
    
    # if existing, retrieves requestQueue
    queue = sqs.get_queue_by_name(QueueName = 'requestQueue')
    
    # sends message in the requestQueue
    queue.send_message(MessageBody = message)

def readMessage():
""" takes no argument, returns nothing, prints the response, allows the client to read responses of the server """
    waiting = "Waiting for a response"
    response = ""
    print(waiting, end="\r")
    
    # seeks for the response of the server
    while response == "" :
        # initiates a connection 
        sqs = boto3.resource('sqs')
        
        # if existing, retrieves responseQueue
        queue = sqs.get_queue_by_name(QueueName = 'responseQueue')
        messages_to_delete = []
        
        # gets the messages in the queue, adds it in the response variable and adds id and receipt_handle in the messages_to_delete list
        for message in queue.receive_messages(MaxNumberOfMessages = 10):
            response = message.body
            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })

        # deletes read messages from the queue
        if len(messages_to_delete) != 0:
            queue.delete_messages(Entries=messages_to_delete)
            
        # prints waiting text
        else: 
            waiting += "."
            print(waiting, end="\r")

    #prints response of the server
    print("\n\n",response,"\n")

def purgeResponses():
""" takes no argument, returns nothing, allows the client to purge the queue"""
    purged = 0
    
    # initiates a connection 
    sqs = boto3.resource('sqs')
    
    # if existing, retrieves responseQueue
    queue = sqs.get_queue_by_name(QueueName = 'responseQueue')
    messages_to_delete = []
    
    # gets the messages in the queue, adds id and receipt_handle in the messages_to_delete list
    for message in queue.receive_messages(MaxNumberOfMessages = 10):
        messages_to_delete.append({
            'Id': message.message_id,
            'ReceiptHandle': message.receipt_handle
        })
        
        # increments number of purged elements
        purged += 1
     
    # deletes messages from the queue
    if len(messages_to_delete) != 0:
        queue.delete_messages(Entries=messages_to_delete)

    # prints the number of purged elements
    print("Purged {} messages.\n\n".format(purged))


def main():
    while True:
        
        # Menu of the client application 
        print("1 - Automatic pre made message")
        print("2 - Automatic random message")
        print("3 - Manually entered message")
        print("4 - Purge queue")
        print("0 - Exit\n\n")
        mode = input("choix : ")

        # 0 - Exit option
        if mode == "0":
            break

        # 1 - Automatic pre made message option
        elif mode == "1" : 
            message = '1,5,22,33,9,0,-15,8,22,100,33,62,90,150,1,2,3'

        # 2 - Automatic random message option
        elif mode == "2": 
            length = input("longueur de la liste : ")
            message = ""
            for i in range(int(length)) : 
                message += str(randint(-100,100)) + str(",")
            message = message[:-1]

        # 3 - Manually entered message option
        elif mode == "3": 
            message = inputMessage()
        
        # 4 - Purge queue option
        elif mode == "4":
            purgeResponses()

        else :
            print("invalid answer...")
            continue

        # does not send message if purge message option has been selected
        if mode != "4": 
            print("Envoi de : \n", message, "\n")
            
            # sending
            try :
                chronoStart = time()
                sendMessage(message)
            
            # error management
            except Exception as e:
                print("### ERROR : sending message has failed ###")
                print(e, "\n\n")
                continue

            # reading
            try :
                readMessage()
                chronoStop = time()
                print("request treated within {:1.3f} secondes\n".format(chronoStop-chronoStart))
            
            # error management
            except Exception as e:
                print("### ERROR : receiving message has failed ###")
                print(e, "\n\n")
                continue

# running the previous code
print('\n### PROGRAM INITIALIZED ###')
purgeResponses()
main()
print('\n### PROGRAM TERMINATED ###\n')
