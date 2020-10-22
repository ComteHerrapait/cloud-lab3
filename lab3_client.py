# Client

import boto3
from time import sleep

def createMessage():

    message=""
    for i in range(20):
        print("Entrer un entier")
        e=input()
        if (i!=19):
            message+=str(e)+","
        else:
            message+=str(e)
    
    return message

def sendMessage():

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName = 'requestQueue')
    #message = createMessage()
    message = '1,5,22,33,9,0,-15,8,22,100,33,62,90,150,1,2,3'
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
        print('\rWaiting for answer')
        sleep(1)
        readMessage()

def main():

    sendMessage()
    readMessage()

print('yo')
main()