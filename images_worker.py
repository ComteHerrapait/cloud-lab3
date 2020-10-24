import boto3
import os
from PIL import Image

def imgProcess(image):
    """Function to modify the image"""
    # Open image by knowing path 
    img = Image.open(image)  

    # Convert to grayscale
    gray = img.convert('1')

    # Save the result in another file
    gray.save('result.png')

def main():
    """Main function. Starts by connecting to two different queues and then process the correct image"""
    # Connection to the queues
    try:
        sqs = boto3.resource('sqs')
        imageInbox = sqs.get_queue_by_name(QueueName = 'imageInbox')
        imageOutbox = sqs.get_queue_by_name(QueueName = 'imageOutbox')
    except Exception as e:
        print("### ERROR : impossible de se connecter aux servers SQS ###")
        print(e, "\n\n")
        exit(-1)
    
    # While loop for processing the requests
    while True:
        messageList = []
        messages_to_delete = []

        # Get messages in imageInbox
        for message in imageInbox.receive_messages(MaxNumberOfMessages = 10):
            print(message.body)
            try:
                #Download the correct image if it exists, then processes it and uploads it
                s3 = boto3.resource('s3')
                pathUnprocessed = 'images/unprocessed/{}'.format(message.body)
                s3.meta.client.download_file('lab3-bucket9', pathUnprocessed, message.body)
                messageList.append(message.body)
                imgProcess(message.body)
                pathProcessed = 'images/processed/{}'.format(message.body)
                s3.meta.client.upload_file('result.png', 'lab3-bucket9', pathProcessed)

            except Exception as e:
                imageOutbox.send_message(MessageBody = '?Error. {}'.format(e))

            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })

            #Removes the images if they exist
            if os.path.exists("result.png"):
                os.remove("result.png")
            
            if os.path.exists(message.body):
                os.remove(message.body)

        # delete messages to remove them from SQS queue
        if len(messages_to_delete) != 0:
            imageInbox.delete_messages(Entries=messages_to_delete)
        
        else:
            print('No Request to Process')
        
        #Send the name of the modified image to the Outbox queue if necessary
        if len(messageList) != 0:
            for message in messageList:
                try:
                    imageOutbox.send_message(MessageBody = message)
                    break
                except Exception as e:
                    imageOutbox.send_message(MessageBody = 'Wrong input')
                    print(e)

main()