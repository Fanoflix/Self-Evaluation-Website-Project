import os
import time

#run this file to automatically setup db and courses and run the server......


#DONT RUN THIS FILE EVERYTIME OR IT RESET THE DB
os.system('python execute_migration.py')
time.sleep(3)
os.system('python setupdb.py')
time.sleep(1)
os.system('python app.py')











