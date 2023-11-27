import os
import sys
import subprocess
import psycopg2
import datetime

from database import *
from InquirerPy import inquirer
# import inquirer


def main():

    # environment variables
    HOME = os.environ.get('HOME')

    # connects to postgresql server
    subprocess.run(["pg_ctl", "-D", f"{HOME}/bankproj", "-o","'-k /tmp'", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("POSTGRESQL SERVER STARTED")

    # to test, change 'database' and 'user' values:
    # to find these values, log in to your postgresql and type '\conninfo'
    # ex. 
    # mandyzhou=# \conninfo
    # You are connected to database "mandyzhou" as user "mandyzhou" via socket in "/tmp" at port "8888".
    conn = psycopg2.connect(database = 'mandyzhou', user = 'mandyzhou', host = '/tmp', port = '8888')

    cur = conn.cursor()

    # sign up / login
    print('Welcome to the ASU Bank!')
    entry = inquirer.select(
        message='Select:',
        choices=['Log In', 'Sign Up']
    ).execute()

    if entry == 'Log In':
        customer = login(cur, HOME)

    if entry == 'Sign Up':
        customer = sign_up(cur)

    # actions
    action = 'Start'
    while action != 'Log Out/Quit':
        action = inquirer.select(
            message='Select Action:',
            choices=['Open a New Bank Account', 'Deposit', 'Withdraw', 'Send Money', 'Check Transaction History', 'Check Current Balance', 'Log Out/Quit']
        ).execute()

        if action == 'Open a New Bank Account':
            print("Open a New Bank Account [action]")

        if action == 'Deposit':
            print('Deposit [action]')
        
        if action == 'Withdraw':
            print('Withdraw [action]')

        if action == 'Send Money':
            print('Send Money [action]')

        if action == 'Check Transaction History':
            print('Check Transaction History [action]')

        if action == 'Check Current Balance':
            print('Check Current Balance [action]')
    
    conn.commit()
    conn.close()

    # quits connection to postgresql server
    print("Logging out...")
    quit(HOME)
        
def login(cur, HOME):
    '''
    require : c_id (customer_id) and password
    task    : find matching customer in database, else retry login, signup, or exit
    return  : Customer object
    '''
    print("LOGIN -------------")
    
    # Customer ID must be numbers ONLY
    c_id = int(inquirer.text(
        message='Enter Customer ID:',
        validate=lambda c_id: c_id.isdigit(),
        invalid_message='Customer ID must be numbers only.'
    ).execute())

    password = inquirer.secret(
        message='Enter Password:'
    ).execute()

    # check database for key match
    # (correct) ex. SELECT * from Customer WHERE c_id=7 and password='2003'

    cur.execute(f"SELECT * from Customer WHERE c_id={c_id} AND password='{password}'")
    result = cur.fetchall() # [(7, '2003', 'Mandy', 'Zhou', datetime.date(2003, 5, 23))]

    # only 1 unique result / Customer account
    if len(result) == 1:
        print("Successfully logged in -------------") 
        customer = Customer(c_id, password, result[0][2],result[0][3],result[0][4])
    
    # no result
    else:
        print("Incorrect login -------------")
        entry = inquirer.select(
            message='Select: ',
            choices=['Retry Log In', 'Sign Up', 'Quit']
        ).execute()

        if entry == 'Retry Log In':
            customer = login(cur, HOME)

        if entry == 'Sign Up':
            customer = sign_up(cur)
        
        if entry == 'Quit':
            quit(HOME)
            sys.exit(1)

    return customer

def sign_up(cur):
    '''
    require : N/A
    task    : collect user input for Customer attributes (first_name, last_name, birthday, password)
              create c_id
              create Customer object
              INSERT INTO new Customer object
    return  : Customer object
    '''

    # user input

    first_name = inquirer.text(
        message='Enter First Name:'
    ).execute()

    last_name = inquirer.text(
        message='Enter Last Name:'
    ).execute()

    birthday = inquirer.text(
        message='Enter Birthday (YYYY-MM-DD):',
        validate=validate_birthday,
        invalid_message='Birthday is invalid. ex. 2003-05-23'
    ).execute()

    password = inquirer.secret(
        message='Enter Password:'
    ).execute()
    
    # get current count of Customer_ID
    # (to then assign next available Customer ID to new Customer)
    cur.execute("SELECT COUNT(c_id) from Customer")
    c_id_length = int(cur.fetchall()[0][0]) # [(9,)] --> 9

    # create new Customer
    customer = Customer(c_id_length+1, password, first_name, last_name, birthday)
    
    # insert new Customer into database
    cur.execute(
        f"""
        INSERT INTO Customer (c_id, password, first_name, last_name, birthday)
        VALUES ({customer.c_id}, '{customer.password}', '{customer.first_name}', '{customer.last_name}', '{customer.birthday}')
        """)

    return customer

def quit(HOME):
    subprocess.run(["pg_ctl", "-D", f"{HOME}/bankproj", "stop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('POSTGRESQL SERVER STOPPED')
    sys.exit(1)

if __name__ == "__main__":
    main()
    

