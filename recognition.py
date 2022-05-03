import boto3
import json
import urllib.request
import urllib.parse
import urllib.error
if __name__ == "__main__":

    bucket = 'lightsailphotos'
    collectionId = 'EFP_Collection-1'
    fileName = urllib.parse.unquote_plus(['Records'][0]['s3']['object']['key'])
    threshold = 98
    maxFaces = 2
    client = boto3.client('rekognition')

    response = client.search_faces_by_image(CollectionId=collectionId,
                                            Image={'S3Object': {'Bucket': bucket, 'Name': fileName}},
                                            FaceMatchThreshold=threshold,
                                            MaxFaces=maxFaces)

    faceMatches = response['FaceMatches']
    print('Matching faces')
    for match in faceMatches:
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print
