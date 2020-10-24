# Report
Here is the report on how we created our application. It is meant to present be a complement of the video and to explain how it works.

## Summary
This project was a two-part project. The first objective of it was to create a client-server application for numbers processing : min, max, mean and median computings. The second part was a client-server application for upload, download and image processing.

### Numbers processing
In order to make our project stable and fucntionable, we had to create two queues (request and response) for the client and the server (both opened on different terminals). We used the AWS Command Line Interface to create those queues and an EC2 instance. You'll find all the commands we used [there].

The client posts a message that goes in the requestQueue. The server gets the message in this queue and then processes it before putting the result in the responseQueue. Finally, the client connects to the responseQueue to get its processed message.

We have several options for the client. The user can either freely choose a message to send, or use a pre-built one, or use a random one and choose its length. If there is a problem in the queue, the user can purge it to delete all messages.

### Image processing

[there]: https://github.com/ComteHerrapait/cloud-lab3/#cloud-lab3-CLI-script
## cloud-lab3 CLI script



Create ec2 instance :

	aws ec2 create-security-group --group-name cloudGroup --description "This is the security group for lab 3"

	aws ec2 authorize-security-group-ingress --group-name cloudGroup --protocol tcp --port 22 --cidr 0.0.0.0/0

	aws ec2 run-instances --image-id ami-0947d2ba12ee1ff75 --security-group-ids sg-0ce27f553870306c8 --instance-type t2.micro --key-name lab3-key

Create four sqs queues :

	aws sqs create-queue --queue-name requestQueue --attributes file://create-queue.json

	aws sqs create-queue --queue-name responseQueue --attributes file://create-queue.json
	
	aws sqs create-queue --queue-name imageInbox --attributes file://create-queue.json
	
	aws sqs create-queue --queue-name imageOutbox --attributes file://create-queue.json

Content of create-queue.json :
	
	{
  		"DelaySeconds": "1",
  		"MessageRetentionPeriod": "3600",
  		"ReceiveMessageWaitTimeSeconds": "1",
  		"VisibilityTimeout": "1"
	}
	
Create s3 bucket :

	aws s3api create-bucket --bucket lab3-bucket9 --region us-east-1

Install the correct packages on the ec2 instance after connecting with putty :

	sudo yum update
	sudo yum install python3
	curl -O https://bootstrap.pypa.io/get-pip.py
   	python3 get-pip.py --user
	pip install boto3 statistics datetime
	pip install awsebcli --upgrade --user
	pip install image
	aws configure

Launch the python script :

	python3 numbers_client.py
	python3 images_client.py

Install tmux to allow the script to run even after putty has been shut down :

	tmux new -s server-lab3
	tmux a -t server-lab3
	tmux new -s server2-lab3
	tmux a -t server2-lab3
