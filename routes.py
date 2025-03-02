from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db, bcrypt
from models import User, RigOperation

# Helper function to check authentication
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


@app.route('/')
def home():
    return "Welcome to RigOps Manager!"

# Dashboard Route (Protected)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    return "Welcome to the Dashboard!"


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user by username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# API Endpoints for Rig Operations

# Create a new rig operation
@app.route('/api/operations', methods=['POST'])
def create_operation():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    operation = RigOperation(name=name, description=description, user_id=user.id)
    db.session.add(operation)
    db.session.commit()

    return jsonify({
        'id': operation.id,
        'name': operation.name,
        'description': operation.description,
        'user_id': operation.user_id
    }), 201

# Get all rig operations for the current user
@app.route('/api/operations', methods=['GET'])
def list_operations():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    operations = RigOperation.query.filter_by(user_id=user.id).all()
    result = [{
        'id': op.id,
        'name': op.name,
        'description': op.description,
        'user_id': op.user_id
    } for op in operations]

    return jsonify(result), 200

# Update a rig operation
@app.route('/api/operations/<int:id>', methods=['PUT'])
def update_operation(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    operation = RigOperation.query.get_or_404(id)
    if operation.user_id != user.id:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json()
    operation.name = data.get('name', operation.name)
    operation.description = data.get('description', operation.description)

    db.session.commit()

    return jsonify({
        'id': operation.id,
        'name': operation.name,
        'description': operation.description,
        'user_id': operation.user_id
    }), 200

# Delete a rig operation
@app.route('/api/operations/<int:id>', methods=['DELETE'])
def delete_operation(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    operation = RigOperation.query.get_or_404(id)
    if operation.user_id != user.id:
        return jsonify({'error': 'Forbidden'}), 403

    db.session.delete(operation)
    db.session.commit()

    return jsonify({'message': 'Operation deleted successfully'}), 200