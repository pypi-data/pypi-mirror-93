# Woodder
A really simple python logger configurator.
It does two things: 
* Formats your logs according to: `%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s`
* Creates a `logs` directory, where it puts all the logs for each run of the application.

## Usage
Here's how you use it:
```
# In a file named: sample_logging.py
import logging
TODO: put wooder import


if __name__ == '__main__':
    project_name = "my_project"
    log_dir = "my_logs"
    Woodder.configure_logging(project_name, log_dir=log_dir)

    logger = logging.getLogger("my-logger")

    logger.info("some info")
    logger.debug("some debug")
    logger.warning("some debug")
    logger.critical("some critical")
    logger.error("some error")
```

Output:
```
2021-02-02 23:23:33,878 - my-logger - sample_logging.py - INFO - some info
2021-02-02 23:23:33,878 - my-logger - sample_logging.py - DEBUG - some debug
2021-02-02 23:23:33,878 - my-logger - sample_logging.py - WARNING - some debug
2021-02-02 23:23:33,879 - my-logger - sample_logging.py - CRITICAL - some critical
2021-02-02 23:23:33,879 - my-logger - sample_logging.py - ERROR - some error
```
