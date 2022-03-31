import psycopg2
hostname = 'localhost'
database = 'flask_db'
username ='postgres'
pwd = 'Rajesh@#76671'
port_id  = 5432
conn = None
cur = None

try:
    conn=psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password =pwd,
        port = port_id)
    cur = conn.cursor()
    create_script = '''CREATE TABLE IF NOT EXISTS employs(
                           id     int PRIMARY KEY,
                           name   varchar(40) NOT NULL,
                           dept_id varchar(50)) 
                           '''
    cur.execute(create_script)


    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
