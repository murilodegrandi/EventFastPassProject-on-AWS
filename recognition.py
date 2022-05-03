import boto3


if __name__ == "__main__":

    region = "us-east-1"
    bucket = 'lightsailphotos'
    collectionId = 'Event-FastPass'
    fileName = 'murilo.jpg'
    threshold = 99
    maxFaces = 2
    
    try:
        
        client = boto3.client('rekognition', region_name=region)
        
        response = client.search_faces_by_image(CollectionId=collectionId,
                                                Image={'S3Object': {'Bucket': bucket, 'Name': fileName}},
                                                FaceMatchThreshold=threshold,
                                                MaxFaces=maxFaces)
        
        faceMatches = response['FaceMatches']
        print('Search Completed! The User has been Identified.\n\n')
        for match in faceMatches:
            print('FaceId:' + match['Face']['FaceId'])
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print(response)
            print(faceMatches)
        
        #Send SNS Topic 
        
        # Create an SNS client
        client = boto3.client('sns', region_name=region)
        sns_resource = boto3.resource("sns", region_name=region)
        # Create the topic if it doesn't exist (this is idempotent)
        #topic = client.create_topic(Name="notifications")
        #topic_arn = topic['TopicArn']  # get its Amazon Resource Name
        # Publish a message.
        client.publish(Message="Good news everyone!", TopicArn="arn:aws:sns:us-east-1:656214810243:GuestCheck-InAlert")
        
 
           
    except NameError:
        print("Error processing object {} from bucket {}. ".format(filename, bucket) + "Make sure your object and bucket exist and your bucket is in the same region as this function.")
    
        