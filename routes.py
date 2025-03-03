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
    if 'user_id' in session:
        # If the user is logged in, redirect to the dashboard
        return redirect(url_for('dashboard'))
    else:
        # If the user is not logged in, redirect to the login page
        flash('Please log in to continue.', 'info')
        return redirect(url_for('login'))

# Dashboard Route (Protected)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    # Fetch all rig operations for viewing
    operations = RigOperation.query.all()
    return render_template('dashboard.html', operations=operations)


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
@app.route('/create-operation', methods=['GET', 'POST'])
def create_operation():
    user = get_current_user()
    if not user:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        rig_name = request.form['rig_name']
        progress = float(request.form.get('progress', 0.0))
        status = request.form.get('status', "-")

        # Validate input
        if not name or not rig_name:
            flash('Name and Rig Name are required.', 'danger')
            return redirect(url_for('create_operation'))

        operation = RigOperation(
            name=name,
            description=description,
            rig_name=rig_name,
            progress=progress,
            status=status,
            user_id=user.id
        )
        db.session.add(operation)
        db.session.commit()

        flash('Rig operation created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_operation.html')

# Edit a rig operation
@app.route('/edit-operation/<int:id>', methods=['GET', 'POST'])
def edit_operation(id):
    user = get_current_user()
    if not user:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    operation = RigOperation.query.get_or_404(id)
    if operation.user_id != user.id:
        flash('You are not authorized to edit this operation.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        operation.name = request.form['name']
        operation.description = request.form['description']
        operation.rig_name = request.form['rig_name']
        operation.progress = float(request.form['progress'])
        operation.status = request.form['status']

        db.session.commit()
        flash('Rig operation updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_operation.html', operation=operation)

# Delete a rig operation
@app.route('/delete-operation/<int:id>', methods=['POST'])
def delete_operation(id):
    user = get_current_user()
    if not user:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    operation = RigOperation.query.get_or_404(id)
    if operation.user_id != user.id:
        flash('You are not authorized to delete this operation.', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(operation)
    db.session.commit()

    flash('Rig operation deleted successfully!', 'success')
    return redirect(url_for('dashboard'))