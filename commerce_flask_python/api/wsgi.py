# this is the entry point
#python3 web.py from terminal in this directory loads instead of flask run to help with debugging
from api import create_app

app = create_app()
# https://stackoverflow.com/questions/1973373/why-does-it-do-this-if-name-main

if __name__ == "__main__":
    app.run(debug =True)