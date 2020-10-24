# Client

import boto3
from time import time

def uploadImage(path):
    """uploads an image to the bucket"""
    try:
        pathTrim = str(path.split("/")[-1])
        pathTrim = str(pathTrim.split("\\")[-1])
        
        distantPath = "images/unprocessed/{}".format(pathTrim)
        s3 = boto3.resource('s3')
        response = s3.meta.client.upload_file(path, 'lab3-bucket9', distantPath)
    except Exception as e:
        print("### ERROR : unable to connect to S3 ###")
        print(e, "\n\n")
        exit(-1)
    return response

def requestProcess(message):
    """sends a request to process an image via a Queue"""
    try:
        sqs = boto3.resource('sqs')
        inQueue = sqs.get_queue_by_name(QueueName = 'imageInbox')
        inQueue.send_message(MessageBody = message)
    except Exception as e:
        print("### ERROR : unable to connect to SQS (in)###")
        print(e, "\n\n")
        exit(-1)

def purgeImages():
    """removes un processed images to avoid client/worker desync"""
    purged = 0

    sqs = boto3.resource('sqs')
    outQueue = sqs.get_queue_by_name(QueueName = 'imageOutbox')
    messages_to_delete = []
    while True:
        for message in outQueue.receive_messages(MaxNumberOfMessages = 10):
            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })
            purged += 1
        if len(messages_to_delete) != 0:
            outQueue.delete_messages(Entries=messages_to_delete)
        else:
            break

    print("Purged {} messages.\n\n".format(purged))


def readResponse():
    """gets the last image in the response queue"""
    try:
        sqs = boto3.resource('sqs')
        outQueue = sqs.get_queue_by_name(QueueName = 'imageOutbox')
    except Exception as e:
        print("### ERROR : unable to connect to SQS (out)###")
        print(e, "\n\n")
        exit(-1)

    waiting = "en attente de réponse"
    response = ""
    print(waiting, end="\r")

    while response == "" :
        messages_to_delete = []
        for message in outQueue.receive_messages(MaxNumberOfMessages = 10):
            response = message.body
            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })

        if len(messages_to_delete) != 0:
            outQueue.delete_messages(Entries=messages_to_delete)
        else: #waiting text
            waiting += "."
            print(waiting, end="\r")

    if "?Error" in response :
        print("\nThe processing has failed : {}\n".format(response))
    else :        
        print("\nImage has been processed : {}".format(response))
        print("Downloading image")
        downloadImage(response)

def downloadImage(name=""):
    if name == "":
        displayFolder("images/processed/")
        name = input("enter the name of the file to download : ")
    try :
        s3 = boto3.resource('s3')
        s3.meta.client.download_file('lab3-bucket9', "images/processed/{}".format(name),name)
    except Exception as e:
        print("### ERROR : unable to download this file")
        print(e)

def displayFolder(path):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('lab3-bucket9')
    for my_bucket_object in my_bucket.objects.filter(Prefix=path):
        path = str(my_bucket_object.key)
        name = path.split("/")[-1]
        if name != "":
            print(" - {}".format(name))

def main():
    while True:
        print("\n\n1 - upload an image")
        print("2 - process an image")
        print("3 - download an image")
        print("4 - purge queue")
        print("0 - quitter\n\n")
        mode = input("select : ")

        if mode == "0":
            break

        elif mode == "1" : #upload an image
            i = input("path of you image : ")
            r = uploadImage(i)
        
        elif mode == "2": #process an image
            displayFolder("images/unprocessed/")
            i = input("name of the image : ")
            requestProcess(i)
            readResponse()
        
        elif mode == "3": #download an image
            downloadImage()

        elif mode == "4": #purge queue
            purgeImages()

        else :
            print("invalid answer...")
            continue


print('\n### PROGRAM INITIALIZED ###')
purgeImages()
main()
print('\n### PROGRAM TERMINATED ###\n')