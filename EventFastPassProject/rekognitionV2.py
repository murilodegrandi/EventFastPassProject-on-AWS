#This script is responsible for the image recognition.

import boto3

collectionId = 'Event-FastPass2'
region = "us-east-1"
photo = 'check.jpg'
threshold = 99
maxFaces = 1
client = boto3.client('rekognition', region_name=region)

BUCKET_NAME = 'search4photobucket' # our photo upload S3 bucket
KEY = 'check.jpg' # name of the image to download

s3 = boto3.resource('s3')


try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'check.jpg')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

try:
    with open(photo, 'rb') as image:
        response = client.search_faces_by_image(CollectionId=collectionId,
        Image={'Bytes': image.read()},
        FaceMatchThreshold=threshold, MaxFaces=maxFaces)
        
    faceMatches = response['FaceMatches']
    print(faceMatches)

    for match in faceMatches:
        print('FaceId:' + match['Face']['FaceId'])
        print('ImageId:' + match['Face']['ImageId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print('Confidence: ' + str(match['Face']['Confidence']))
    
    #Send SNS Topic to the Event admin to inform whether the guest is allowed or not.

    # Create an SNS client
    client = boto3.client('sns', region_name=region)
    sns_resource = boto3.resource("sns", region_name=region)
        
    # Publish a message.
    client.publish(Message="Facial Recognition Successful!\n\nSimilarity: " + 
    "{:.2f}".format(match['Similarity']) + "% \n" + 'Confidence: ' + str(match['Face']['Confidence']) + 
    '\n Please click here to scan ticket: https://eventfastpass.link/scan', 
    TopicArn="arn:aws:sns:us-east-1:656214810243:GuestCheck-InAlert")

except NameError as e:
    print('Facial Recognition completed.\nResult = Not found')
     #Send SNS Topic 

    # Create an SNS client
    client = boto3.client('sns', region_name=region)
    sns_resource = boto3.resource("sns", region_name=region)
        
    # Publish a message.
    client.publish(Message="<<<Identity not found!>>>\n\n This person does not have authorization to attend the event!", 
    TopicArn="arn:aws:sns:us-east-1:656214810243:GuestCheck-InAlert")


    


