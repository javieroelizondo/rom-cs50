# RigOps Manager
RigOps Manager is a Flask-based application for managing rig operations.
*** Feel free to contribute, report issues, or suggest improvements on GitHub! ***

## Link to video:
> [!CAUTION]
> Pending to generate and upload a video to youtube for CS50.

## Table of Contents

* Versions
* Project Structure
* Design Choices
* Future Enhancements
* How to Run

## Versions
### v0
- Initial configuration

### v1
- User authentication (registration, login, logout).
- CRUD API endpoints for managing rig operations.

### v2
- All logged-in users can view all rig operations.
- Only the owner of a rig operation can modify or delete it.
- Added `Progress %`, `Status`, and `Rig Name` fields to rig operations.
- Frontend implemented using Python + Jinja templates.


# Project Structure
The project is organized into the following files and folders:

## Files
### app.py :
The main entry point of the application.
    Initializes the Flask app and configures settings like SECRET_KEY for session management.
    Sets up the database using SQLAlchemy.
    Imports routes from routes.py to define all endpoints.
    Starts the Flask development server when executed.

> [!NOTE]
> Use SQLAlchemy to simplify the coding and to be able to implement the back end with SQL or no-SQL in the future. SQLAlchemy can handle the sqlite database creation.
> On the other hand, If the sqlite code directly, It'd be less flexible. 

### SQLite Database :
-   Stores user accounts and rig operations.
-   Tables include user and rig_operation.

### routes.py :
Contains all the routes for the application, including authentication, CRUD operations, and dashboard functionality.
    Defines routes for user authentication (/register, /login, /logout).
    Implements CRUD functionality for rig operations (/create-operation, /edit-operation/id, /delete-operation/id).
    Includes authorization checks to ensure only the owner of a rig operation can modify or delete it.
    Redirects unauthenticated users to /login and sets / as the default route to redirect to /login.

### models.py :
Defines the database schema using SQLAlchemy.
Includes models for User and RigOperation.
    - User: Stores user information (e.g., username, hashed password).
    - RigOperation: Represents rig operations with fields like name, description, rig_name, progress, status, and user_id (foreign key linking to the User model).

### templates/ :
Contains HTML templates rendered by Jinja.
Files include base.html, dashboard.html, create_operation.html, edit_operation.html, login.html, and register.html.
    - base.html : The base template that includes Bootstrap CSS, navigation bar, and flash messages.
    - dashboard.html : Displays a table of all rig operations with options to create, edit, or delete operations (for owners only).
    - create_operation.html : Form for creating new rig operations.
    - edit_operation.html : Form for editing existing rig operations.
    - login.html : Login form for user authentication.
    - register.html : Registration form for new users.

### static/ :
**Empty** Only contains the screenshot for this README file.

### requirements.txt :
Lists all Python dependencies required to run the application.
    Specifies libraries like Flask, Flask-Bcrypt, and SQLAlchemy.

### README.md :
This file, which documents the project.


# Design Choices
1. User Authentication
I implemented user authentication using Flask sessions to ensure secure access to protected routes.
Passwords are hashed using Flask-Bcrypt to prevent plaintext storage in the database.
2. Data Privacy
While all logged-in users can view all rig operations, only the creator of an operation can modify or delete it. This ensures data privacy and prevents unauthorized changes.
3. Frontend with Jinja
For v2, I chose to implement the front end using Python + Jinja templates instead of AJAX for simplicity. This approach allows users to interact with the application without requiring advanced JavaScript knowledge.
Future versions will include AJAX for dynamic updates and a more interactive user experience. Furthermore, implement React components to only render dynamic components and not the whole webpage.
4. Database Schema
The RigOperation model was extended to include Progress %, Status, and Rig Name fields to provide more context and functionality for managing rig operations.


# Future Enhancements
## AJAX Integration :
Replace Jinja-based forms with dynamic AJAX requests for creating, updating, and deleting rig operations.
Improve responsiveness and reduce page reloads.

## Styling :
Use TailwindCSS to create a modern and visually appealing UI.

## User Roles :
Add admin and regular user roles for better access control.
***Admins*** could have the ability to manage all rig operations, while regular ***users*** would only manage their own.

## Deployment :
Deploy the application to a cloud platform like Heroku or Render for public access.

## Additional Features :
Add filtering and sorting options to the dashboard for better usability.
Implement real-time notifications using WebSockets.
Implement a v2 of the dashboard including a dynamic Gantt chart as the main graphic.


# How to Run
1. Clone the repository:
    git clone https://github.com/javieroelizondo/rom-cs50.git
    cd rom-cs50

2. Set up a virtual environment:
    python -m venv venv
    venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Initialize database:
    python
    from app import app, db
    with app.app_context():
        db.create_all()

    exit()

5. Run the application:
    python app.py

6. Access the Application:
    Open your browser and navigate to http://127.0.0.1:5000/

> [!TIP]
> Follow the recommended format

## Recommended format for creating rig operations

**Type:**   Field used to describe the type of operation *(future version will change the name of the column to Type, and implement a pop-up list to select from it)* 
        Recommended to define coherent abreviations like:  DRL (drilling), CON (completion), WO (workover), ABN (abandonment)

> [!IMPORTANT]
> The field name and database labe of the rig operations is still NAME. The **Type** change was only update on the HTML output. Pending to change the **form** and **database structure**.

**Rig Name:** Field used to describe the name of the well or location.
        Recommended to generate name with the format NNN-### using three letters for an abreviation of the field name (e.g. PCD ~ Cerro Dragon) and three numbers to define a rig in that field.
        
> [!WARNING]
> The Rig Name is a UNIQUE identifier of a well.

**Description:** A short description of the activity to be executed at the rigsite.

![Screenshot of some added rig operations.](https://github.com/javieroelizondo/rom-cs50/blob/main/static/Screenshot.png)
