import boto3
from io import BytesIO
from PIL import Image

class S3_Connector:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.s3_bucket = self.s3_resource.Bucket(self.bucket_name)

    def move(self, dir_old, dir_new, file_name):
        " Moves an object to other directory"

        old_destination = f'{dir_old}/{file_name}'
        new_destination = f'{dir_new}/{file_name}'
        copy_source = {
                        'Bucket': self.bucket_name,
                        'Key': old_destination}
        self.s3.copy_object(CopySource=copy_source, Bucket=self.bucket_name, Key=new_destination)
        self.s3.delete_object(Bucket=self.bucket_name, Key=old_destination)

        return True

    def upload_img(self, img, dir, file_name):
        " Uploads an image to specified directory"

        self.s3.upload_fileobj(img, self.bucket_name, f'{dir}/{file_name}')

        return True

    def read_images(self, dir):
        " Reads images from S3 directory"

        imgs = []
        for img in self.s3_bucket.objects.filter(Prefix=dir):
            file_path = img.key
            if file_path.endswith('.png'):
                image_data = BytesIO()
                self.s3_bucket.download_fileobj(img.key, image_data)
                image = Image.open(image_data)

                # Insert file name
                image.filename = img.key.split('/')[-1]
                imgs.append(image)
        
        return imgs
    
    def count_objects(self, dir):
        " Counts objects in S3 directory"

        count_objects = self.s3_bucket.objects.filter(Prefix=dir)

        return len(list(count_objects)) -1


BUCKET_NAME = 'tflmhelloworldbucket'
s3_conn = S3_Connector(BUCKET_NAME)