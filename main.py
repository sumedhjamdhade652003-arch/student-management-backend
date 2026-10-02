import psycopg2

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException

app=FastAPI()
connection= psycopg2.connect(
    host='localhost',
    port='5432',
    database='postgres',
    user='postgres',
    password ='postgres'
)

cursor=connection.cursor()
class Student(BaseModel):
    id:int
    name:str
    course:str
# get all student 
@app.get('/students')
def get_all_students():
    cursor.execute('select * from students')
    rows=cursor.fetchall()

    result=[]
    for row in rows:
        result.append({
            'id':row[0],
            'name':row[1],
            'course':row[2]
        })
    return result

# get single student
@app.get('/students/{id}')
def get_single_student(id:int):
    try:
        cursor.execute ('select * from students where id=%s',(id,))
        row=cursor.fetchone()
        return{
            'id':row[0],
            'name':row[1],
            'course':row[2]
        }
    except:
        raise httpException(status_code=404,detail='Invalid Student Id')

# create student record
@app.post('/students')


def create_student_record(student: Student):
    try:
        cursor.execute('insert into students (id,name,course) values (%s,%s,%s)',(student.id,student.name,student.course))
        connection.commit()
        raise HTTPException(status_code=201,detail='Student Record Created Successfully')
    except psycopg2.IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=404,detail='Student ID already exists')