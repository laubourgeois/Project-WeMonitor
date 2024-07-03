# create a separate constant.py file
# Get the current working directory
import os

URLS_FILE_PATH=os.path.join(os.getcwd(), 'src/wemonitor/data/urls.txt')
FILE_LOG=os.path.join(os.getcwd(), 'src/wemonitor/data/logs.txt')
CERT_FOLDER=os.path.join(os.getcwd(), 'src/wemonitor/certs')