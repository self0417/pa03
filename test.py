import unittest
from app import app, db, Task
from kata import fizzbuzz

class TestKata(unittest.TestCase):
    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(3), "Fizz")
        self.assertEqual(fizzbuzz(5), "Buzz")
        self.assertEqual(fizzbuzz(15), "FizzBuzz")

class TestORM(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_task_creation(self):
        with app.app_context():
            task = Task(description="Test")
            db.session.add(task)
            db.session.commit()
            self.assertEqual(Task.query.count(), 1)
    
    def test_empty_description_fails(self):
        with self.assertRaises(ValueError):  
            Task(description="")
    
    def test_get_tasks_endpoint(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()