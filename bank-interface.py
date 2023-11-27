import subprocess
import os
import psycopg2

HOME = os.environ.get('HOME')
subprocess.run(["pg_ctl", "-D", f"{HOME}/bankproj", "-o","'-k /tmp'", "start"], stdout=subprocess.DEVNULL)
print("server started:")

conn = psycopg2.connect(database = 'mandyzhou',
                        user = 'mandyzhou',
                        host = '/tmp',
                        port = '8888')

cur = conn.cursor()

cur.execute("SELECT * from Customer;")
result = cur.fetchall()
print(result)

print("---")

cur.execute("""
INSERT INTO Customer (c_id, password, first_name, last_name, birthday)
VALUES (9, '2004', 'Jasmine', 'Situ', '2004-06-18');
""")
cur.execute("SELECT * from Customer;")
result = cur.fetchall()
print(result)

conn.commit()
conn.close()

subprocess.run(["pg_ctl", "-D", f"{HOME}/bankproj", "stop"], stdout=subprocess.DEVNULL)
print("server stopped.")

