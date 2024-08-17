from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from password import my_password
from marshmallow import fields, ValidationError, validate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@localhost/fitness_center'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    age = fields.Integer(required=True, validate=validate.Range(min=1))
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ('name', 'age', 'email', 'phone', 'id')

class WorkoutSessionSchema(ma.Schema):
    member_id = fields.Integer(required=True, validate=validate.Range(min=1))
    session_date = fields.String(required=True, validate=validate.Length(min=1))
    session_time = fields.Integer(required=True, validate=validate.Range(min=1))
    activity = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        fields = ('member_id', 'session_date', 'session_time', 'activity', 'session_id')

# Instantiate schemas
member_schema = MemberSchema()
members_schema  = MemberSchema(many=True)

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema  = WorkoutSessionSchema(many=True)

class Member(db.Model):
    __tablename__ = 'Members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(320))
    phone = db.Column(db.String(15))
    sessions = db.relationship('WorkoutSession', passive_deletes=True, backref='member')#Establishes relationship with members and workoutSessions as a collection (list)

class WorkoutSession(db.Model):
    __tablename__ = 'WorkoutSessions'
    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id', ondelete='Cascade'))
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.String(255), nullable=False)

# member routes
@app.route('/members', methods=['GET'])
def get_member():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route('/members/<int:id>', methods=['GET'])
def get_member_by_id(id):
    member = Member.query.get_or_404(id)
    return member_schema.jsonify(member)

@app.route('/members', methods=['POST'])
def add_member():
    try:
        # Validate and deserialize input
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_member = Member(name=member_data['name'], age=member_data['age'], email=member_data['email'], phone=member_data['phone'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'New member added successfully'}), 201

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    member.name = member_data['name']
    member.age = member_data['age']
    member.email = member_data['email']
    member.phone = member_data['phone']
    db.session.commit()
    return jsonify({'message': 'Member details updated successfully'}), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member removed successfully'}), 300

# workout_session routes
@app.route('/sessions', methods=['GET'])
def get_workout_session():
    workout_sessions = WorkoutSession.query.all()
    return workout_sessions_schema.jsonify(workout_sessions)

@app.route('/sessions/<int:id>', methods=['GET'])
def get_workout_session_by_session_id(id):
    session = WorkoutSession.query.get_or_404(id)
    return workout_session_schema.jsonify(session)

@app.route('/sessions_by_member/<int:id>', methods=['GET'])
def get_workout_sessions_by_member(id):
    workout_sessions = WorkoutSession.query.filter_by(member_id = id)
    return workout_sessions_schema.jsonify(workout_sessions)

@app.route('/sessions', methods=['POST'])
def add_workout_session():
    try:
        # Validate and deserialize input
        workout_session_data = workout_session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_workout_session = WorkoutSession(
        member_id=workout_session_data['member_id'], 
        session_date=workout_session_data['session_date'], 
        session_time=workout_session_data['session_time'], 
        activity=workout_session_data['activity'])
    db.session.add(new_workout_session)
    db.session.commit()
    return jsonify({'message': 'New workout session added successfully'}), 201

@app.route('/sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    workout_session = WorkoutSession.query.get_or_404(id)
    try:
        workout_session_data = workout_session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    workout_session.member_id = workout_session_data['member_id']
    workout_session.session_date = workout_session_data['session_date']
    workout_session.session_time = workout_session_data['session_time']
    workout_session.activity = workout_session_data['activity']
    db.session.commit()
    return jsonify({'message': 'Workout session details updated successfully'}), 200

@app.route('/sessions/<int:id>', methods=['DELETE'])
def delete_workout_session(id):
    workout_session = WorkoutSession.query.get_or_404(id)
    db.session.delete(workout_session)
    db.session.commit()
    return jsonify({'message': 'Workout session removed successfully'}), 300


# Initialize the database and create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)