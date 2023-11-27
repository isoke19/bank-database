import os
import subprocess
import psycopg2

from InquirerPy import inquirer

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

    conn.commit()
    conn.close()

    # sign up / login
    entry = inquirer.select(
        message='Welcome to the ASU Bank! Select:',
        choices=['Log In', 'Sign Up']
    ).execute()

    if entry == 'Log In':
        customer = login()

    if entry == 'Sign Up':
        customer = sign_up()

    # actions

    action = 'Start'
    while action != 'Log Out':
        action = inquirer.select(
            message='Select Action:',
            choices=['Open a New Bank Account', 'Deposit', 'Withdraw', 'Send Money', 'Check Transaction History', 'Check Current Balance', 'Log Out']
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
    
    print('Logging out...')

    # quits connection to postgresql server
    subprocess.run(["pg_ctl", "-D", f"{HOME}/bankproj", "stop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("POSTGRESQL SERVER STOPPED")

def login():
    '''
    require : c_id (customer_id) and password
    task    : find matching customer in database, else return error or sign up
    return  : Customer object
    '''
    return 'customer_obj_placeholder_from_log_in'

def sign_up():
    '''
    require : N/A
    task    : collect user input for Customer attributes (first_name, last_name, birthday, password)
              create c_id
              create Customer object
    return  : Customer object
    '''
    return 'customer_obj_placeholder_from_sign_up'

if __name__ == "__main__":
    main()
    

