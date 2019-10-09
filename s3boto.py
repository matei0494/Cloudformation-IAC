'''
https://realpython.com/python-boto3-aws-s3/
'''

import uuid
import boto3
import boto3
import sys
import os
from os import listdir
from os.path import isfile, join
import os




s3_resource = boto3.resource('s3')
client = boto3.client('s3')


def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])


def create_bucket(bucket_prefix, s3_connection):
    ''' S3 connection is the boto3.resource instantiation, s3_resource in our case '''
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response



def create_temp_file(size,file_name,file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]),file_name])
    with open(random_file_name,'w') as f:
        f.write(str(file_content) * size)
    with open(random_file_name,'r') as file:
        text = file.read()
        
    return text, random_file_name
    


def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name,file_name).copy(copy_source)



def list_files():
    mypath = 'C:\\Users\\matei.stanescu\\Desktop\\udacity'
    # onlyfiles = [f for f in listdir(mypath)]
    # return(onlyfiles)
    onlyfiles = listdir(mypath)
    for i in range(len(onlyfiles)):
        print(onlyfiles[i])


def menu():
    print("************MAIN MENU**************")
    
    choice = input("""
                      A: Create a bucket
                      B: Create a file
                      C: Copy a file from a bucket to another
                      D: Upload a file to a bucket
                      E: Download a file from a bucket
                      F: Delete a file from a bucket
                      Q: Quit/Log Out

                      Please enter your choice: """)

    if choice == "A" or choice =="a":
        input_bucket_name = input('What is the bucket prefix? ')
        create_bucket(input_bucket_name)

    elif choice == "B" or choice =="b":
        input_file_size = int(input('What is the file size? '))
        input_file_prefix = input('What is the file prefix? ')
        input_file_content = input('What is the content of the file? ')
        created_file = create_temp_file(input_file_size,input_file_prefix,input_file_content)
        print('File {} has been crated and it has the following content: {}'.format(created_file[1],created_file[0]))

    elif choice == "C" or choice =="c":
        input_bucket_source = input('What is the source bucket? ')
        input_bucket_destination = input('What is the destination bucket? ')
        input_file_name = input('What is the file you want to transfer? ')
        copy_to_bucket(input_bucket_source,input_bucket_destination,input_file_name)

    
    elif choice=="D" or choice=="d":
        response = client.list_buckets()
        print('Your buckets are: \n' )
        for i in range(len(response['Buckets'])):
            print(response['Buckets'][i]['Name'])
        print('\n')
        print('Your files are:\n' )
        list_files()
        print('\n')
        input_bucket_name = input('What is the bucket you want to upload your file to? ')
        input_file_name = input('What is the file you want to upload? ')
        first_object = s3_resource.Object(bucket_name=input_bucket_name, key=input_file_name)
        first_object.upload_file(input_file_name)

    elif choice == "E" or choice =="e":
        response = client.list_buckets()
        print('Your buckets are: \n' )
        for i in range(len(response['Buckets'])):
            print(response['Buckets'][i]['Name'])
        
        input_bucket_name = input('What is the bucket you want to download from?')
        rez = client.list_objects(Bucket=input_bucket_name)
        print('The following files are in your bucket: \n')
        for i in range(len(rez['Contents'])):
            print(rez['Contents'][i]['Key'])
        print('\n')   
        input_file_name = input('What is the file you want to download? ')
        s3_resource.Object(input_bucket_name, input_file_name).download_file(f'C:/Users/matei.stanescu/Desktop/udacity/{input_file_name}')

    elif choice == "F" or choice =="f":
        
        response = client.list_buckets()
        print('Your buckets are: \n' )
        for i in range(len(response['Buckets'])):
            print(response['Buckets'][i]['Name'])
        
        input_bucket_name = input('What is the bucket you want to delete an object from? ')
        rez = client.list_objects(Bucket=input_bucket_name)
        print('The following files are in your bucket: \n')
        for i in range(len(rez['Contents'])):
            print(rez['Contents'][i]['Key'])
        print('\n')   
        input_file_name = input('What is the file you want to delete ? ')
        s3_resource.Object(input_bucket_name, input_file_name).delete()

    elif choice=="Q" or choice=="q":
        sys.exit

    else:
        print("You must only select either A,B,C, or D.")
        print("Please try again")



menu()









