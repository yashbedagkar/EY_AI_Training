import yaml
import logging

logging.basicConfig(
    filename="app2.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

config = {
    "app":
        {"name": "Student",
        "Portal version": 1.0},
    "database":
        {"host": "localhost",
        "port": 3306,
        "user": "root"}
}


with open("config2.yaml", "w") as f:
    yaml.dump(config, f)
logging.info("File created and data added to it")

try:
    with open("config2.yaml", "r") as f:
        data = yaml.safe_load(f)
    logging.info("File read")
    print(f"Connecting to {data['database']['host']}:{data['database']['port']} as {data['database']['user']}")
except FileNotFoundError as e:
    print(e)
    logging.error(f"Error occurred {e}")



