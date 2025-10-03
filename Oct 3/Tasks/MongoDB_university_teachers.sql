use university
switched to db university
db.teachers.insertOne({
  teacher_id : 1,
  name : "Dr. Mehta",
  age : 45,
  city : "Mumbai",
  subject : "AI",
  salary : 90000
})
{
  acknowledged: true,
  insertedId: ObjectId('68dfb7345b80eb030518ed1b')
}
db.teachers.insertMany([
  {teacher_id: 2, name: "Prof. Sharma", age: 50, city: "Delhi", subject: "ML", salary: 95000},
  {teacher_id: 3, name: "Ms. Reddy", age: 38, city: "Hyderabad", subject: "Data Science", salary: 87000},
  {teacher_id: 4, name: "Mr. Das", age: 40, city: "Kolkata", subject: "AI", salary: 88000},
  {teacher_id: 5, name: "Dr. Khan", age: 47, city: "Bengaluru", subject: "ML", salary: 99000}
])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfb7445b80eb030518ed1c'),
    '1': ObjectId('68dfb7445b80eb030518ed1d'),
    '2': ObjectId('68dfb7445b80eb030518ed1e'),
    '3': ObjectId('68dfb7445b80eb030518ed1f')
  }
}
db.teachers.find()
{
  _id: ObjectId('68dfb7345b80eb030518ed1b'),
  teacher_id: 1,
  name: 'Dr. Mehta',
  age: 45,
  city: 'Mumbai',
  subject: 'AI',
  salary: 90000
}
{
  _id: ObjectId('68dfb7445b80eb030518ed1c'),
  teacher_id: 2,
  name: 'Prof. Sharma',
  age: 50,
  city: 'Delhi',
  subject: 'ML',
  salary: 95000
}
{
  _id: ObjectId('68dfb7445b80eb030518ed1d'),
  teacher_id: 3,
  name: 'Ms. Reddy',
  age: 38,
  city: 'Hyderabad',
  subject: 'Data Science',
  salary: 87000
}
{
  _id: ObjectId('68dfb7445b80eb030518ed1e'),
  teacher_id: 4,
  name: 'Mr. Das',
  age: 40,
  city: 'Kolkata',
  subject: 'AI',
  salary: 88000
}
{
  _id: ObjectId('68dfb7445b80eb030518ed1f'),
  teacher_id: 5,
  name: 'Dr. Khan',
  age: 47,
  city: 'Bengaluru',
  subject: 'ML',
  salary: 99000
}
db.teachers.findOne({name: "Dr. Mehta"})
{
  _id: ObjectId('68dfb7345b80eb030518ed1b'),
  teacher_id: 1,
  name: 'Dr. Mehta',
  age: 45,
  city: 'Mumbai',
  subject: 'AI',
  salary: 90000
}
db.teachers.find({salary: {$gt: 90000}})
{
  _id: ObjectId('68dfb7445b80eb030518ed1c'),
  teacher_id: 2,
  name: 'Prof. Sharma',
  age: 50,
  city: 'Delhi',
  subject: 'ML',
  salary: 95000
}
{
  _id: ObjectId('68dfb7445b80eb030518ed1f'),
  teacher_id: 5,
  name: 'Dr. Khan',
  age: 47,
  city: 'Bengaluru',
  subject: 'ML',
  salary: 99000
}
db.teachers.find({}, {name: 1, subject: 1, _id: 0})
{
  name: 'Dr. Mehta',
  subject: 'AI'
}
{
  name: 'Prof. Sharma',
  subject: 'ML'
}
{
  name: 'Ms. Reddy',
  subject: 'Data Science'
}
{
  name: 'Mr. Das',
  subject: 'AI'
}
{
  name: 'Dr. Khan',
  subject: 'ML'
}
db.teachers.updateOne(
  {name: "Mr. Das"},
  {$set: {salary: 92000, subject: "Advanced AI"}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
db.teachers.updateMany(
  {subject: "ML"},
  {$set: {bonus: 5000}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 2,
  modifiedCount: 2,
  upsertedCount: 0
}
db.teachers.deleteOne({name: "Ms. Reddy"})
{
  acknowledged: true,
  deletedCount: 1
}
db.teachers.deleteMany({salary: {$lt: 88000}})
{
  acknowledged: true,
  deletedCount: 0
}
university
Selection deleted

