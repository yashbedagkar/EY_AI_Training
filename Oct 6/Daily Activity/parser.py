import configparser

config = configparser.ConfigParser()

config["database"] ={
    "host" : "localhost",
    "port" : "27017",
    "user" : "root",
"password" : "admin123"

}

with open("app.ini", "w") as configfile:
    config.write(configfile)

config.read("app.ini")
print(config["database"]["host"])