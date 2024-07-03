import logging
import os
import re  # To import the regex module
import requests
import threading #To handle non-blocking input for stopping the loop
import time
import wemonitor.constants as const
from kafka import KafkaProducer

# Function to check the health status of a website that the user enters
def check_health_status():
    url = input("Enter a Website URL to check its health status (ex:https://www.google.fi): ")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"The URL is healthy, status code {response.status_code}")
            with open(const.URLS_FILE_PATH, 'a') as file:
                file.write(f"{url}\n")  # Write the input URL directly

            retry = input("Add another Website URL or Exit? (add/exit): ")
            if retry.lower() == "add":
                check_health_status()
            else:
                with open(const.URLS_FILE_PATH, 'r') as file:
                    content = file.read()
                    logging.info("List of verified websites:")
                    logging.info(content)
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        retry = input("Please, insert a URL web address format, Retry or Exit? (r/e) ")
        if retry.lower() == "r":
            check_health_status()
        else:
            logging.info("Exiting.")
            SystemExit

# Function to check the response time of the websites listed in the urls.txt file 
def collect_logs(regex_pattern=None):
    results = []  # To store results for sending to Kafka
    try:
        with open(const.URLS_FILE_PATH, 'r') as file:
            urls = file.readlines()
    except FileNotFoundError:
        logging.error(f"File {const.URLS_FILE_PATH} not found.")
        return

    for url in urls:
        url = url.strip()
        try:
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            response_time = end_time - start_time

            log_message = f"Website {url}: Status code: {response.status_code}, Response time: {response_time:.4f} seconds"

            if regex_pattern:
                match = re.search(regex_pattern, response.text)
                if match:
                    log_message += " (Regex match found)"
                    regex_result = True
                else:
                    log_message += " (No regex match found)"
                    regex_result = False
                logging.info(f"Checked for regex pattern: {regex_pattern}")

            with open(const.FILE_LOG, 'a') as log_file:
                log_file.write(log_message + "\n")
            
            logging.info(log_message)
            time.sleep(2)
            
            # Collect the result to send to Kafka
            results.append({
                "url": url,
                "status_code": response.status_code,
                "response_time": response_time,
                "regex_match": regex_result if regex_pattern else None
            })

        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred while checking the response time for {url}: {e}")
            time.sleep(2)
    return results

# Function to send the logs to Kafka topic
def send_logs_to_kafka():
    with open(f'{const.FILE_LOG}', 'r') as file:
        logs = file.readlines()
   
    TOPIC_NAME = 'website-logs'
    producer = KafkaProducer(
        bootstrap_servers="kafka-fi-elekta-d752.d.aivencloud.com:14807",
        security_protocol="SSL",
        ssl_cafile=os.path.join(const.CERT_FOLDER, 'ca.pem'),
        ssl_certfile=os.path.join(const.CERT_FOLDER, 'service.cert'),
        ssl_keyfile=os.path.join(const.CERT_FOLDER, 'service.key'),
    )
    
    if producer:
        for log in logs:
                log = log.strip()
                producer.send(TOPIC_NAME, log.encode('utf-8'))
                # Slow down the log display
                time.sleep(1) 
        producer.close()
        logging.info("Logs sent successfully.")
    else:
        logging.error("Failed to send logs.")
        SystemExit

def schedule_checks():
    try:
        interval_minutes = int(input("Enter the interval (in minutes) for how often you want to check the sites: "))
        interval_seconds = interval_minutes * 60
        logging.info(f"Scheduled to check the sites every {interval_minutes} minutes.")
        
        stop_flag = threading.Event()
        
        def check_for_stop():
            while not stop_flag.is_set():
                stop_input = input("Press 's' to stop the periodic check and exit the process: ")
                if stop_input.lower() == 's':
                    stop_flag.set()
        
        stop_thread = threading.Thread(target=check_for_stop)
        stop_thread.start()
        
        while not stop_flag.is_set():
            logging.info("Starting site checks...")
            collect_logs()
            send_logs_to_kafka()
            logging.info(f"Waiting for {interval_minutes} minutes until the next check.")
            
            for second in range(interval_seconds):
                if stop_flag.is_set():
                    break
                if second % 5 == 0:
                    logging.info("Press 's' + 'Enter' to stop the periodic check and exit the process.")
                time.sleep(1)
        
        stop_flag.set()
        stop_thread.join()
        logging.info("Stopping periodic checks.")
    
    except ValueError:
        logging.error("Please enter a valid number for the interval.")
        schedule_checks()
    
# Function to delete logs.txt and urls.txt files
def delete_files():
    if os.path.exists(const.FILE_LOG) and os.path.exists(const.URLS_FILE_PATH):
        os.remove(const.FILE_LOG)
        os.remove(const.URLS_FILE_PATH)
        print("Temporary logs files deleted successfully.")
    else:
        print("Temporary logs files not found. Deletion skipped.")
    

