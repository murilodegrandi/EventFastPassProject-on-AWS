import boto3

if __name__ == "__main__":

    region = "us-east-1"
    bucket = 'rekogpicturess3'
    collectionId = 'EFP_Collection-1'
    fileName = 'sergio.jpg'
    threshold = 70
    maxFaces = 2

    client = boto3.client('rekognition', region_name=region)

    response = client.search_faces_by_image(CollectionId=collectionId,
                                            Image={'S3Object': {'Bucket': bucket, 'Name': fileName}},
                                            FaceMatchThreshold=threshold,
                                            MaxFaces=maxFaces)

    faceMatches = response['FaceMatches']
    print('Matching faces')
    for match in faceMatches:
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print(response)
        print(faceMatches)