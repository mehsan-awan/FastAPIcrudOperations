from fastapi import APIRouter
from models.student import Student
from config.database import conn
from schemas.student import student_entity, list_of_student_entity
from bson import ObjectId
student_router = APIRouter()


# Get one student
@student_router.get('/students/{studentid}')
async def find_one_student(studentid):
    return student_entity(conn.local.student.find_one({'_id': ObjectId(studentid)}))

# Get all students
@student_router.get('/students')
async def find_all_students():
    return list_of_student_entity(conn.local.student.find())


# Create student
@student_router.post('/students')
async def create_student(student: Student):
    conn.local.student.insert_one(dict(student))
    student = student.dict()
    student["msg"] = "Success"
    return student


# Update Student
@student_router.put('/students/{studentid}')
async def update_student(studentid, student: Student):
    conn.local.student.find_one_and_update(
        {'_id': ObjectId(studentid)},  # Find the student
        {'$set': dict(student)}        # Update the data
    )
    return student_entity(conn.local.student.find_one(studentid))


# Delete Student
@student_router.delete('/students/{studentid}')
async def delete_student(studentid):
    # conn.local.student.find_one_and_delete(studentid)
    return student_entity(conn.local.student.find_one_and_delete({'_id': ObjectId(studentid)}))
