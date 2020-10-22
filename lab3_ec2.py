# EC2
 
import boto3
import statistics
from time import sleep
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
    sqs = boto3.resource('sqs')
    requestQueue = sqs.get_queue_by_name(QueueName = 'requestQueue')
    responseQueue = sqs.get_queue_by_name(QueueName = 'responseQueue')

    file = open("log.txt", 'r+')
    while True:
        messageList = []
        messages_to_delete = []
        for message in requestQueue.receive_messages(MaxNumberOfMessages = 10):
            print(message.body)
            file.write(message.body)
            messageList.append(message.body)
            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })

        # delete messages to remove them from SQS queue
        if len(messages_to_delete) != 0:
            delete_response = requestQueue.delete_messages(
                Entries=messages_to_delete)
        
        else:
            print('Empty')
        
        if len(messageList) != 0:
            for message in messageList:
                result = process(message)
                responseQueue.send_message(MessageBody = result)

        sleep(5)



main()


    




