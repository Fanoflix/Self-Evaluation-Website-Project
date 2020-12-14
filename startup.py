import os
import time

#run this file to automatically setup db and courses and run the server......


#DONT RUN THIS FILE EVERYTIME OR IT RESET THE DB
os.system('python execute_migration.py')
time.sleep(5)
os.system('python setupdb.py')
os.system('python app.py')

