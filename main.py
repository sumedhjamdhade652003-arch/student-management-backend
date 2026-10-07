import psycopg2

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
load_dotenv()
import os

app=FastAPI()
connection= psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cursor=connection.cursor()
class Student(BaseModel):
    id:int = None
    name:str = None
    course:str = None
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
        raise HTTPException(status_code=404,detail='Invalid Student Id')

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
    
# update student record
@app.put('/students/{id}')
def update_student_record(id: int, student: Student):
    cursor.execute('update students set id=%s,name=%s,course=%s where id=%s',(student.id,student.name,student.course,id))
    if(cursor.rowcount==0):
        raise HTTPException(status_code=404,detail='Invalid Student Id')
    connection.commit()
    raise HTTPException(status_code=200,detail='Student Record Updated Successfully')

#update partial record
@app.patch('/students/{id}')
def update_partial_student_record(id: int, student: Student):
    if(student.name!=None):
        cursor.execute('update students set name=%s where id=%s',(student.name,id))
    if(student.id!=None):
        cursor.execute('update students set id=%s where id=%s',(student.id,id))
    if(student.course!=None):
        cursor.execute('update students set course=%s where id=%s',(student.course,id))
    if(cursor.rowcount==0):
        raise HTTPException(status_code=404,detail='Invalid Student Id')
    connection.commit()
    raise HTTPException(status_code=200,detail='partial update Successfully')

#delete student record
@app.delete('/students/{id}')
def delete_student_record(id:int):
    cursor.execute('delete from students where id=%s',(id,))
    if(cursor.rowcount==0):
        raise HTTPException(status_code=404,detail='Invalid Student Id')
    connection.commit()
    raise HTTPException(status_code=200,detail='Student Record Deleted Successfully')