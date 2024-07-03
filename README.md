<span style="color: #1A1A2E;">

<br/><br/>

## WeMonitor

<img src="./WeMonitor/src/wemonitor/data/wemonitor-logo.png" alt="WeMonitor" width="600"/>

## Overview

WeMonitor is a scalable Aiven Python web monitor application that feeds information about website availability to an Aiven Kafka instance.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](WeMonitor/LICENSE.txt) file for details.

## Context

This project has been implemented on MacOS using the latest Kafka-Python package version (2.0.2) and its **upper compatible** Python version (3.8.10). WeMonitor is expexted to be working in this specifc intended environment. The use of different environment versions can lead to possible discrepancies that are not taken into account in this project.

## Installation prerequisites

Step 1: Download Python `3.8.10` for your [platform](https://www.python.org/downloads/release/python-3810/)\
Step 2: Run the Installer\
Step 3: Open a terminal window and verify the installation

```
$ python3 --version
Python 3.8.10 # Success!
```


The Python installer for macOS include pip. Make sure pip is up-to-date.

```
python3 -m pip install --upgrade pip
python3 -m pip --version
```

## Installation 


- Clone this Git repository

- Open a Terminal and `cd` to the `WeMonitor` source directory you just created with the clone command
```
cd WeMonitor/
```

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install WeMonitor __locally__.
```
pip install .
```

## Usage

To run the script with different options from the command line.

- Copy the issued Kafka private key to certs folder
  ```
  cd WeMonitor
  cp ~/path-to-private-key/service.key src/wemonitor/certs
  ```

- **Run the health check of a given site:**
  ```bash
  python3 run.py --health
  ```

- **Run the health check and fetch logs of a given site:**
  ```bash
  python3 run.py --health --fetch
  ```

- **Run the health check, verify if the response body matches the optional regex pattern :**
  ```
  python3 run.py --health --fetch --regex "<your-regex-pattern>"
  ```
  
- **Run the health check, fetch logs, and send logs to Kafka instance of a given site:**
  ```bash
  python3 run.py --health --fetch --send
  ```

- **Run the health check, fetch logs, send logs with regex option to Kafka and schedule periodical checks:**
  ```
  python3 run.py --health --fetch --regex "<your-regex-pattern>" --send --schedule
  ```

- **Run with a specific logging level:**
  ```bash
  python3 run.py --health --fetch --send --schedule --log-level DEBUG
  ```
  Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.

#### Follow the prompt instructions


  - To monitor one Website
  ```
  $ python3 run.py "<Argument1>" "<Argument2>" ....
  ...
  Enter a Website URL to check its health status (ex:https://www.google.fi): https://www.aiven.io
  ```

  - To monitor additional Website
  ```
  Add another Website URL or Exit? (add/exit):add
  ....
  Enter a Website URL to check its health status (ex:https://www.google.fi): https://www.priceline.com
  ```

Keep adding Website until you're done. Once you finish, **exit** for the script to continue.

#### Command-Line Arguments

- `--health`: Health check the sites
- `--fetch`: Fetch logs for the sites
- `--regex "<your-regex-pattern>"`: Whether the specified regex pattern was found in the response body of monitored URLs.
- `--send`: Send logs to Kafka Aiven instance
- `--schedule`: Schedule periodic log collection & sending to Kafka instance (every 1 minute if not stated)
- `--log-level`: Set the logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)



#### Example

To check the health status, fetch logs, and send logs to Kafka with debug logging:

```bash
python3 run.py --health --fetch --send --log-level DEBUG
```

## Shipping

- Install **wheel** (Library to generate built-package binay format for Python) and **sdist** (library to generate source `.tar.gz` distribution). The wheel project provides the bdist_wheel command for setuptools to generate binary.
```
pip install wheel sdist
```

- Generate Binary & source distribution package
```
python3 setup.py bdist_wheel sdist
```

Binary file is located in `WeMonitor/build`\
Distribution file is located in `WeMonitor/dist`

## Testing Strategy

This chapter provides details about the unit tests implemented in the **test_wemonitor.py** file. These tests verify the functionality of the wemonitor module in the WeMonitor application. The tests utilize the unittest framework and various mocking techniques to isolate dependencies and ensure reliable and repeatable testing.

**Unit Tests:** These tests focus on testing individual components of the wemonitor module in isolation. Mocking is used to replace external dependencies such as network requests and file operations with controlled responses.

**Mocking**: The unittest.mock module is extensively used to mock:

- External HTTP requests (requests.get)
- File operations (open) for reading and writing

**Integration Tests:** Although not explicitly covered in this file, integration tests would typically verify interactions between different components of the application, such as verifying Kafka message production and file system operations.

### Running Tests

To run the Unit tests defined in **test_wemonitor.py**, follow these steps:

- Clone this repository
- Go to the project root directory
  ```
  cd WeMonitor
  ```
- Install the required dependencies
  ```
  pip install -r requirements.txt
  ```
- Set the PYTHONPATH so that Python recognizes the src directory
  ```
  export PYTHONPATH=$(pwd)/src
  ```
- Run all unit tests. This command discovers and executes all test cases defined in the test folder.
  ```
  python3 -m unittest discover -s src/tests
  ```

## Development

To test out code changes, you’ll need to build WeMonitor from source, which requires a C/C++ compiler and Python environment.

Step 1: Create an isolated environment

* Make sure that you have cloned this repository
* `cd` to the `WeMonitor` source directory you just created with the clone command

Step 2: Unix/macOS with Virtual Environment

**Virtualenv** is a tool to set up your Python environments. Since Python 3.3, it has been integrated into the standard library under the __venv__ module. If you don't have it running, you can install it  by running `pip install virtualenv`:

Consult the documentation for setting up **virtualenv** if needed [here](https://docs.python.org/3/library/venv.html).

```
Create a new virtual environment. Use an ENV_DIR of your choice. For instance:~/Users/<yourname>/.pyenv/versions wemonitor.
$ python3 -m venv wemonitor-dev-1.0.1

# Activating the virtual environment to put the virtual environment-specific python and pip executables into your shell’s PATH.
$ source wemonitor-dev-1.0.1/bin/activate

# To confirm the virtual environment is activated, check the location of your Python interpreter:
$ which python
wemonitor-dev-1.0.1/bin/python # Success!   

# Install required dependencies in the virtual environment
$ pip install -r requirements.txt

# De-activate the virtual environment
deactivate 

# Delete Virtual environment
rm -rf ./wemonitor-dev-1.0.1
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change. 

Please make sure to update tests as appropriate.
</span>



