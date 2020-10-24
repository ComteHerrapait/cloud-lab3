# EC2
 
import boto3
import statistics
import os
from datetime import datetime

def parser(message):
    '''Splits the numbers by "," to process them. Returns a list of integers'''
    msgList=message.split(",")
    intList=[]
    for i in range(len(msgList)):
        intList.append(int(msgList[i]))
    intList.sort()
    return(intList)
    
    
def minimum(intList):
    '''Computes the minimum of an integer list'''
    return intList[0]

def maximum(intList):
    '''Computes the maximum of an integer list'''
    return intList[-1]

def average(intList):
    '''Computes the mean of an integer list'''
    return statistics.mean(intList)

def median(intList):
    '''Computes the median of an integer list'''
    return statistics.median(intList)

def process(message):
    '''Uses previous functions to process the input message. Returns the results'''
    intList = parser(message)
    minList = minimum(intList)
    maxList = maximum(intList)
    avgList = average(intList)
    medList = median(intList)

    response = ("""The list minimum is : {} \nThe list maximum is : {} \nThe list average is : {} \nThe list median is : {}"""
                ).format(minList, maxList, avgList, medList)
    
    return response

def main():
    '''Main function. Starts by connecting to two different queues and writes the different requests in a log file'''

    # Check if a log file already exists 
    if os.path.exists("log.txt"):
        os.remove("log.txt")
    
    # Connection to the queues
    try:
        sqs = boto3.resource('sqs')
        requestQueue = sqs.get_queue_by_name(QueueName = 'requestQueue')
        responseQueue = sqs.get_queue_by_name(QueueName = 'responseQueue')
    except Exception as e:
        print("### ERROR : Failed to connect to SQS servers ###")
        print(e, "\n\n")
        exit(-1)

    # Connection to an Amazon S3 bucket to upload the log file
    try:
        s3 = boto3.resource('s3')
        s3.meta.client.download_file('lab3-bucket9', 'log.txt', 'log.txt')
    except Exception as e:
        file = open('log.txt','w')
        s3.meta.client.upload_file('log.txt', 'lab3-bucket9', 'log.txt')

    # While loop for processing the requests
    while True:
        messageList = []
        messages_to_delete = []

        # Get messages in requestQueue
        for message in requestQueue.receive_messages(MaxNumberOfMessages = 10):
            print(message.body)
            date = datetime.now()
            realDate = date.strftime("%d/%m/%Y %H:%M:%S ")

            # Write the message in the log file
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

        # Delete messages to remove them from SQS queue
        if len(messages_to_delete) != 0:
            requestQueue.delete_messages(Entries=messages_to_delete)
        
        else:
            print('No Request to Process')
        
        # Process messages and send the in the responseQueue
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