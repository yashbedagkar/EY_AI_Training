db
test
use university
switched to db university
db.students.insertOne({
  student_id : 1,
  name : "Rahul",
  age : 21,
  city : "Mumbai",
  course : "AI",
  marks : 85
})
{
  acknowledged: true,
  insertedId: ObjectId('68dfa4a12222d5f93a8804da')
}
db.students.insertMany([
  {student_id: 2, name: "Priya", age: 22,city : "Delhi",course:"ML",marks : 90},
  {student_id: 3, name : "Arjun",age : 20,city :"Bengaluru",course: "Data Science", marks : 88},
  {student_id: 4,name : "Neha", age :23 ,city :"Hyderabad",course : "AI",marks: 88},
  {student_id:5,name : "Vikram",age:21,city: "Chennai",course : "ML",marks:95}                      
])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfa8142222d5f93a8804db'),
    '1': ObjectId('68dfa8142222d5f93a8804dc'),
    '2': ObjectId('68dfa8142222d5f93a8804dd'),
    '3': ObjectId('68dfa8142222d5f93a8804de')
  }
}
db.students.find()
{
  _id: ObjectId('68dfa4a12222d5f93a8804da'),
  student_id: 1,
  name: 'Rahul',
  age: 21,
  city: 'Mumbai',
  course: 'AI',
  marks: 85
}
{
  _id: ObjectId('68dfa8142222d5f93a8804db'),
  student_id: 2,
  name: 'Priya',
  age: 22,
  city: 'Delhi',
  course: 'ML',
  marks: 90
}
{
  _id: ObjectId('68dfa8142222d5f93a8804dc'),
  student_id: 3,
  name: 'Arjun',
  age: 20,
  city: 'Bengaluru',
  course: 'Data Science',
  marks: 88
}
{
  _id: ObjectId('68dfa8142222d5f93a8804dd'),
  student_id: 4,
  name: 'Neha',
  age: 23,
  city: 'Hyderabad',
  course: 'AI',
  marks: 88
}
{
  _id: ObjectId('68dfa8142222d5f93a8804de'),
  student_id: 5,
  name: 'Vikram',
  age: 21,
  city: 'Chennai',
  course: 'ML',
  marks: 95
}
db.students.findOne({name:"Rahul"})
{
  _id: ObjectId('68dfa4a12222d5f93a8804da'),
  student_id: 1,
  name: 'Rahul',
  age: 21,
  city: 'Mumbai',
  course: 'AI',
  marks: 85
}
db.students.find({marks:{$gt : 85}})
{
  _id: ObjectId('68dfa8142222d5f93a8804db'),
  student_id: 2,
  name: 'Priya',
  age: 22,
  city: 'Delhi',
  course: 'ML',
  marks: 90
}
{
  _id: ObjectId('68dfa8142222d5f93a8804dc'),
  student_id: 3,
  name: 'Arjun',
  age: 20,
  city: 'Bengaluru',
  course: 'Data Science',
  marks: 88
}
{
  _id: ObjectId('68dfa8142222d5f93a8804dd'),
  student_id: 4,
  name: 'Neha',
  age: 23,
  city: 'Hyderabad',
  course: 'AI',
  marks: 88
}
{
  _id: ObjectId('68dfa8142222d5f93a8804de'),
  student_id: 5,
  name: 'Vikram',
  age: 21,
  city: 'Chennai',
  course: 'ML',
  marks: 95
}
db.students.find({},{name :1,course:1, _id : 0})
{
  name: 'Rahul',
  course: 'AI'
}
{
  name: 'Priya',
  course: 'ML'
}
{
  name: 'Arjun',
  course: 'Data Science'
}
{
  name: 'Neha',
  course: 'AI'
}
{
  name: 'Vikram',
  course: 'ML'
}
db.students.updateOne(
  {name :"Neha"},
  {$set :{marks : 92, course :"Advanced AI"}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
db.students.updateMany(
  {course : "AI"},
  {$set : {grade : "A"}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
db.students.find()
{
  _id: ObjectId('68dfa4a12222d5f93a8804da'),
  student_id: 1,
  name: 'Rahul',
  age: 21,
  city: 'Mumbai',
  course: 'AI',
  marks: 85,
  grade: 'A'
}
{
  _id: ObjectId('68dfa8142222d5f93a8804db'),
  student_id: 2,
  name: 'Priya',
  age: 22,
  city: 'Delhi',
  course: 'ML',
  marks: 90
}
{
  _id: ObjectId('68dfa8142222d5f93a8804dc'),
  student_id: 3,
  name: 'Arjun',
  age: 20,
  city: 'Bengaluru',
  course: 'Data Science',
  marks: 88
}
{
  _id: ObjectId('68dfa8142222d5f93a8804dd'),
  student_id: 4,
  name: 'Neha',
  age: 23,
  city: 'Hyderabad',
  course: 'Advanced AI',
  marks: 92
}
{
  _id: ObjectId('68dfa8142222d5f93a8804de'),
  student_id: 5,
  name: 'Vikram',
  age: 21,
  city: 'Chennai',
  course: 'ML',
  marks: 95
}
db.students.deleteOne({name:"Arjun"})
{
  acknowledged: true,
  deletedCount: 1
}
db.students.deleteMany({marks : {$lt :80}})
{
  acknowledged: true,
  deletedCount: 0
}
university
Selection deleted

