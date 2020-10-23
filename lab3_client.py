# Client

import boto3
from time import sleep
from random import randint
def createMessage():
    message=""
    for i in range(20):
        print("Entrez un entier")
        e=input()
        if (i!=19):
            message+=str(e)+","
        else:
            message+=str(e)
    return message

def inputMessage():
    message = ""
    while True:
        i = input ("nombre(s) {} <- ".format(message))
        if i == "":
            break
        else:
            if len(message) > 0 and message[-1] != ",":
                message += ","
            message += i    
    return message


def sendMessage(message):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName = 'requestQueue')
    queue.send_message(MessageBody = message)

def readMessage():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName = 'responseQueue')
    messageList = []
    messages_to_delete = []
    for message in queue.receive_messages(MaxNumberOfMessages = 10):
        print(message.body)
        messageList.append(message.body)
        messages_to_delete.append({
            'Id': message.message_id,
            'ReceiptHandle': message.receipt_handle
        })
    if len(messages_to_delete) != 0:
        queue.delete_messages(Entries=messages_to_delete)

    else:
        print('\rWaiting for answer', end="\r")
        sleep(1)
        readMessage()

def main():
    while True:
        print("1 - message préfait automatique")
        print("2 - message aléatoire automatique")
        print("3 - message saisi manuelement")
        print("0 - quitter\n\n")
        mode = input("choix : ")

        if mode == "0":
            print('\n### PROGRAM TERMINATED ###\n')
            break
        elif mode == "1" : #message préfait automatique
            message = '1,5,22,33,9,0,-15,8,22,100,33,62,90,150,1,2,3'

        elif mode == "2": #message aléatoire automatique
            length = input("longueur de la liste : ")
            message = ""
            for i in range(int(length)) : 
                message += str(randint(-100,100)) + str(",")
            message = message[:-1]

        elif mode == "3": #message saisi manuelement
            message = inputMessage()
            
        else :
            print("invalid answer...")
            continue

        print("Message envoyé : \n", message, "\n")

        try :
            sendMessage(message)
        except Exception as e:
            print("/!\ ERROR : impossible d'envoyer le message /!\\")
            print(e, "\n\n")
            continue

        readMessage() #reception

print('\n### PROGRAM INITIALIZED ###\n')
main()