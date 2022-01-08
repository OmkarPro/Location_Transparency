from flask import Flask,render_template,request
import mysql.connector
import traceback
import logging

app = Flask(__name__)

@app.route("/")
def hello_world():
    try:
        mydb0 = mysql.connector.connect(host="localhost",user="root",password="",database="department")
        mydb1 = mysql.connector.connect(host="localhost",user="root",password="",database="project")
        mydb2 = mysql.connector.connect(host="localhost",user="root",password="",database="student")

        mycursor0 = mydb0.cursor()
        mycursor1 = mydb1.cursor()
        mycursor2 = mydb2.cursor()

        tableNames = []
        mycursor0.execute("show tables")
        tableNames.append(mycursor0.fetchall())

        mycursor1.execute("show tables")
        tableNames.append(mycursor1.fetchall())

        mycursor2.execute("show tables")
        tableNames.append(mycursor2.fetchall())
        tables=[]
        allcolumns = []
        tablenames=[]
        ntab = []
        try:
            db = [mycursor0,mycursor1,mycursor2]
            # ntab = []
            for i in range(len(db)):
                ntab.append(len(tableNames[i]))
                tabs = []
                temp = []
                col = []
                for j in range(len(tableNames[i])):
                    tabs.append(tableNames[i][j][0])
                    db[i].execute("select * from "+tabs[-1])
                    temp.append(db[i].fetchall())
                    col.append(db[i].column_names)
                tables.append(temp)
                tablenames.append(tabs)
                allcolumns.append(col)
        except:
            print("Error")

    except Exception as e:
            logging.error(traceback.format_exc())
            print("error in fetching records from all tables")

    return render_template('index.html',table=tables,allcolumn=allcolumns,ntab = ntab,tabnames=tablenames)
    

@app.route('/insert', methods=['POST'])
def insert():
    f=0
    if request.method =="POST":
        mydb = -1
        query = request.form['query']
        try:
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor()
            try:
                print("Query is executing")
                print(mycursor.execute(query))
                print(query)
                if 'select' in query.lower():
                    print("SELECT query")
                    records = mycursor.fetchall()
                    columns = mycursor.column_names
                    count = mycursor.rowcount
                    f=1
                    return render_template('base.html',record = records,column=columns, row = count,col=len(columns), flag= f)
                else:
                    mydb.commit()
                    f=2
                    return render_template('base.html',flag=f)
            except Exception as e:
                f=0
                logging.error(traceback.format_exc())
                return render_template('base.html',flag=f)
        except Exception as e:
            logging.error(traceback.format_exc())
            f=3
            return render_template('base.html',flag=f)
# select * from department.department join project.project on department.dept_id=project.project_dept

if __name__=='__main__':
    app.run(debug=True)
