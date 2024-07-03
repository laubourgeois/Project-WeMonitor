import argparse
import logging
from wemonitor.wemonitor import (
    check_health_status,
    collect_logs,
    send_logs_to_kafka,
    schedule_checks,
    delete_files 
)

def setup_logging(log_level):
    # Set up logging to console with the specified log level
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info(f"Logging set to {log_level}")

def parse_arguments():
    # Define the command-line arguments for the application using argparse.ArgumentParser class 
    parser = argparse.ArgumentParser(description='Run the wemonitor application.')
    parser.add_argument(
        '--health-check',
        action='store_true',
        help='Check the health status of the sites'
    )
    parser.add_argument(
        '--fetch',
        action='store_true',
        help='Fetch logs for the sites'
    )
    parser.add_argument(
        '--send',
        action='store_true',
        help='Send logs to Kafka Aiven instance'
    )
    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Schedule periodic log collection and sending to Kafka every 1 minute (default)'
    )
    parser.add_argument(
        '--regex',
        type=str,
        help='Optional regex pattern to check against the response body'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level'
    )
    return parser.parse_args()

def main():
    # Parse the command-line arguments and set up logging with the specified log level 
    args = parse_arguments()
    setup_logging(args.log_level)

    try:
        if args.health_check:
            delete_files()
            logging.info("Checking health status")
            check_health_status()
        
        if args.fetch:
            logging.info("Fetching logs")
            collect_logs(args.regex)
        
        if args.send:
            logging.info("Sending logs to Kafka")
            send_logs_to_kafka()
        
        if args.schedule:
            logging.info("Scheduling log collection and sending to Kafka every 1 minute")
            schedule_checks()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
