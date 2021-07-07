import pandas as pd
import boto3
from io import StringIO

#sudo docker build -t hello-demo . # To build the program
#sudo docker run -it hello-demo NFL_Web.py #To Run the image

session = boto3.Session(
        aws_access_key_id ='',
        aws_secret_access_key='',
        )
s3 = session.resource('s3')

csv_buffer = StringIO()

bucket = 'junk-yard'

url = 'https://www.nfl.com/stats/player-stats/'

df = pd.read_html(url)

df = df[0]

df.to_csv(csv_buffer)

s3.Object(bucket,'Test/df_nfl.csv').put(Body=csv_buffer.getvalue())
~                                                                     
