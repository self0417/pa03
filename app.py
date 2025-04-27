from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<Task {self.id}: {self.description}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

def initialize_database():
    with app.app_context():
        db.create_all()
        if not Task.query.first():
            initial_tasks = [
                Task(description="Aprender ORM", completed=False),
                Task(description="Implementar TDD", completed=True),
                Task(description="Crear pruebas unitarias", completed=False)
            ]
            db.session.bulk_save_objects(initial_tasks)
            db.session.commit()

def example_orm_operations():
    with app.app_context():
 
        new_task = Task(description="Nueva tarea de ejemplo")
        db.session.add(new_task)
        db.session.commit()

        tasks = Task.query.all()
        pending_tasks = Task.query.filter_by(completed=False).all()
        
        task = Task.query.get(1)
        if task:
            task.completed = True
            db.session.commit()

        task_to_delete = Task.query.get(2)
        if task_to_delete:
            db.session.delete(task_to_delete)
            db.session.commit()

if __name__ == '__main__':
    initialize_database()
    example_orm_operations()