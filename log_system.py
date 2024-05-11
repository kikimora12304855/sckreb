import logging
import os

class LogSystem:

    def __init__(self) -> None:

        self.path = "/log" 

        self.path_log = os.path.join(self.path, "app.log")

        file_handler = logging.FileHandler(self.path_log)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logging.root.addHandler(file_handler)


    def save_to_file(self, content):
        with open(os.path.join(self.path, "tmp.txt"), "w") as file:
            file.write(content)


    def read_to_file(self):
        file_path = os.path.join(self.path, "tmp.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
        return None

    def seve_to_log(self, level_logging, message, error):
        """
        B - DEBUG
        I - INFO
        W - WARNING
        E - ERROR
        C - CRITICAL
        """
        message = f"|{message}|:  {error}" 

        match level_logging:
            case "B", "b", "debug":
                logging.debug(message)
                print(message)
            case "I", "i", "info":
                logging.info(message)
                print(message)
            case "W", "w", "warning":
                logging.warning(message)
                print(message)
            case "E", "e", "error":
                logging.error(message)
                print(message)
            case "C", "c", "critical":
                logging.critical(message)
                print(message)
            case _:
                logging.info(message)
                print(message)

