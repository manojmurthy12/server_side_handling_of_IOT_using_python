from flask import *
import psycopg2

app = Flask(__name__)

switch1=True
switch2=True

sqlURI='postgres://hgxchphp:EpLGCsRdkDrdh2NS5LF3qa-P4Ei3ZCBi@arjuna.db.elephantsql.com/hgxchphp'

connection=psycopg2.connect(sqlURI)
try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE values (switchno INT, switchstatus INT);")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO values VALUES (%s,%s);", (1, 1))
            cursor.execute("INSERT INTO values VALUES (%s,%s);", (2, 1))
except psycopg2.errors.DuplicateTable:
    pass


@app.route('/retrievestatus', methods=['GET'])
def switchStatus():
    # search = str(request.args['query'])
    dict={}
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM values;")
            values = cursor.fetchall()
    if values[0][0] == 1 and values[0][1] == 1 :
        dict['switch1']=True;
    if values[0][0] == 1 and values[0][1] == 0 :
        dict['switch1']=False;
    if values[0][0] == 2 and values[0][1] == 1 :
        dict['switch2']=True;
    if values[0][0] == 2 and values[0][1] == 0 :
        dict['switch2']=False;
    # for checking 2nd values
    if values[1][0] == 1 and values[1][1] == 1 :
        dict['switch1']=True;
    if values[1][0] == 1 and values[1][1] == 0 :
        dict['switch1']=False;
    if values[1][0] == 2 and values[1][1] == 1 :
        dict['switch2']=True;
    if values[1][0] == 2 and values[1][1] == 0 :
        dict['switch2']=False;


    return jsonify(dict)



@app.route('/switch1', methods=['GET'])
def changeStatus1():
    search = str(request.args['query'])
    if search == 'on':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE values SET switchstatus=%s WHERE switchno=%s;", (1,1))
                # cursor.execute("INSERT INTO values VALUES (%s,%s);", (1, 1))
        return jsonify('switch1 is on')
    if search == 'off':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE values SET switchstatus=%s WHERE switchno=%s;", (0,1))
        return jsonify('switch1 is off')

@app.route('/switch2', methods=['GET'])
def changeStatus2():
    search = str(request.args['query'])
    if search=='on':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE values SET switchstatus=%s WHERE switchno=%s;", (1,2))
        return jsonify('switch2 is on')
    if search=='off':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE values SET switchstatus=%s WHERE switchno=%s;", (0,2))
        return jsonify('switch2 is off')

if __name__ == '__main__':
    app.run()