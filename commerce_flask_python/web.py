# this is the entry point
from dotenv import load_dotenv
load_dotenv()
import os 
from api import create_app

app = create_app()
# https://stackoverflow.com/questions/1973373/why-does-it-do-this-if-name-main

if __name__ == "__main__":
    # print(os.getenv("AUTH0_DOMAIN"))
    # https://stackoverflow.com/questions/41940663/how-can-i-change-the-host-and-port-that-the-flask-command-uses
    app.run(debug =True, port=6060, host='0.0.0.0')