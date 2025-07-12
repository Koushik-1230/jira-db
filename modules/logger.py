import os
import logging
from datetime import datetime
import glob


class Logger:
    def __init__(self, log_dir="Logs", max_log_files=5):

        self.log_dir = log_dir
        self.max_log_files = max_log_files

        # Create Logs directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Generate log file name with current timestamp
        log_filename = datetime.now().strftime("log_%d_%m_%Y_%H_%M.log")
        self.log_filepath = os.path.join(self.log_dir, log_filename)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(self.log_filepath), logging.StreamHandler()],
        )

        # Delete old logs if necessary
        self._delete_old_logs()

    def _delete_old_logs(self):
        """
        Delete old log files if the number of log files exceeds the limit.
        """
        # Get a list of all log files in the directory
        log_files = glob.glob(os.path.join(self.log_dir, "log_*.log"))

        # Sort files by modification time (oldest first)
        log_files.sort(key=os.path.getmtime)

        # Delete the oldest files if the number of files exceeds the limit
        if len(log_files) > self.max_log_files:
            for old_log in log_files[: len(log_files) - self.max_log_files]:
                os.remove(old_log)
                logging.info(f"Deleted old log file: {old_log}")

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)

    def debug(self, message):
        logging.debug(message)
