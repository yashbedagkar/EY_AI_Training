import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.debug("This is a debug message")
logging.info("Application started")
logging.warning("low memory warning")
logging.error("File not found error")
logging.critical("critical system failure")