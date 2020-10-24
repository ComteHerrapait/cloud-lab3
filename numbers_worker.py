# EC2
 
import boto3
import statistics
import os
from datetime import datetime

# Parser pour récupérer le message sous forme d'une liste d'entiers
def parser(message):
    liste=message.split(",")
    listeEntiers=[]
    for i in range(len(liste)):
        listeEntiers.append(int(liste[i]))
    listeEntiers.sort()
    #print(listeEntiers)
    return(listeEntiers)
    
    
# Calcul du minimum
def minimum(listeEntiers):
    return listeEntiers[0]

# Calcul du maximum
def maximum(listeEntiers):
    return listeEntiers[-1]

# Calcul de la moyenne
def moyenne(listeEntiers):
    return statistics.mean(listeEntiers)
    
# Calcul de la mediane
def mediane(listeEntiers):
    return statistics.median(listeEntiers)

def process(message):
    intList = parser(message)
    minList = minimum(intList)
    maxList = maximum(intList)
    avgList = moyenne(intList)
    medList = mediane(intList)

    response = ("""The list minimum is : {} \nThe list maximum is : {} \nThe list average is : {} \nThe list median is : {}"""
                ).format(minList, maxList, avgList, medList)
    
    return response

def main():

    if os.path.exists("log.txt"):
        os.remove("log.txt")

    try:
        sqs = boto3.resource('sqs')
        requestQueue = sqs.get_queue_by_name(QueueName = 'requestQueue')
        responseQueue = sqs.get_queue_by_name(QueueName = 'responseQueue')
    except Exception as e:
        print("### ERROR : impossible de se connecter aux servers SQS ###")
        print(e, "\n\n")
        exit(-1)

    try:
        s3 = boto3.resource('s3')
        s3.meta.client.download_file('lab3-bucket9', 'log.txt', 'log.txt')
    except Exception as e:
        file = open('log.txt','w')
        s3.meta.client.upload_file('log.txt', 'lab3-bucket9', 'log.txt')

    while True:
        messageList = []
        messages_to_delete = []
        for message in requestQueue.receive_messages(MaxNumberOfMessages = 10):
            print(message.body)
            date = datetime.now()
            realDate = date.strftime("%d/%m/%Y %H:%M:%S ")
            with open("log.txt", "a") as myfile:
                myfile.write(realDate)
                myfile.write(message.body)
                myfile.write('\n')
            s3.meta.client.upload_file('log.txt', 'lab3-bucket9', 'log.txt')
            messageList.append(message.body)
            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })

        # delete messages to remove them from SQS queue
        if len(messages_to_delete) != 0:
            requestQueue.delete_messages(Entries=messages_to_delete)
        
        else:
            print('No Request to Process')
        
        if len(messageList) != 0:
            for message in messageList:
                try:
                    result = process(message)
                    responseQueue.send_message(MessageBody = result)
                    break
                except Exception as e:
                    responseQueue.send_message(MessageBody = 'Wrong input')
                    print(e)

print('\n### PROGRAM INITIALIZED ###\n')
main()
print('\n### PROGRAM TERMINATED ###\n')