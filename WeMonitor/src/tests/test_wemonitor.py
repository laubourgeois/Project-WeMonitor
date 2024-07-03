import unittest
from unittest.mock import patch, MagicMock, mock_open
from wemonitor.wemonitor import (
    check_health_status,
    collect_logs,
    send_logs_to_kafka,
    schedule_checks,
    delete_files
)
import wemonitor.constants as const

# Define the test class and test methods for the wemonitor module functions using the unittest.TestCase class. 
class TestWemonitor(unittest.TestCase):
    #
    @patch('builtins.input', side_effect=['https://www.google.fi', 'exit'])
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    #
    def test_check_health_status(self, mock_open_file, mock_requests_get, mock_input):
        # Mock the response for requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        # Call the function
        with self.assertLogs(level='INFO') as log:
            check_health_status()

        # Verify logging and file write operations
        self.assertIn("INFO:root:The URL is healthy, status code 200", log.output)
        self.assertIn("INFO:root:List of verified websites:", log.output)
        mock_open_file().write.assert_called_once_with('https://www.google.fi\n')
        mock_open_file().read.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='https://www.example.com\n')
    @patch('requests.get')
    # Patching the open function to return a file with a URL
    def test_collect_logs(self, mock_requests_get, mock_open_file):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "This is a test response text."
        mock_requests_get.return_value = mock_response

        with self.assertLogs(level='INFO') as log:
            results = collect_logs()

        # Verify the logs and result
        self.assertIn("INFO:root:Website https://www.example.com: Status code: 200, Response time:", log.output[0])
        self.assertGreater(len(results), 0)

@patch('builtins.open', new_callable=mock_open, read_data='Sample log data\n')
@patch('kafka.KafkaProducer')
@patch('os.path.join', side_effect=lambda *args: '/certs')  # Mock os.path.join for SSL paths
@patch('wemonitor.constants.CERT_FOLDER', '/certs')  # Mock the CERT_FOLDER path
# Patching the open function to return a file with sample log data
def test_send_logs_to_kafka(self, mock_cert_folder, mock_os_path_join, mock_kafka_producer, mock_open_file):
    mock_producer_instance = mock_kafka_producer.return_value
    
    with self.assertLogs(level='INFO') as log:
        send_logs_to_kafka()

    # Verify Kafka send and logging
    self.assertIn("INFO:root:Logs sent successfully.", log.output)
    mock_producer_instance.send.assert_called()
    mock_producer_instance.close.assert_called_once()

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files(self, mock_print, mock_os_remove):
        delete_files()

        # Verify file removal and print calls
        mock_os_remove.assert_any_call(const.FILE_LOG)
        mock_os_remove.assert_any_call(const.URLS_FILE_PATH)
        mock_print.assert_called_with("Temporary logs files deleted successfully.")
        
@patch('time.sleep', return_value=None)  # Mock time.sleep to return immediately
@patch('builtins.input', side_effect=['s'])  # Mock input to simulate user stopping the check
@patch('wemonitor.wemonitor.collect_logs')
@patch('wemonitor.wemonitor.send_logs_to_kafka')

# Patching the input to return 's' to stop the loop immediately
def test_schedule_checks(self, mock_collect_logs, mock_send_logs_to_kafka, mock_input, mock_sleep):
    # Since schedule_checks runs indefinitely, we will mock the parts that make it controllable

    # Patching the input to return 's' to stop the loop immediately
    mock_input.return_value = 's'

    with self.assertLogs(level='INFO') as log:
        schedule_checks()

    # Check if the functions were called at least once
    mock_collect_logs.assert_called_once()
    mock_send_logs_to_kafka.assert_called_once()

    # Check the log output to ensure the process was stopped
    self.assertIn('INFO:root:Stopping periodic checks.', log.output)

if __name__ == '__main__':
    unittest.main()
