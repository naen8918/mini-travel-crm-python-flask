# Mini Travel CRM (Python Flask Project)

This project is a minimal CRM (Customer Relationship Management) system designed for small travel agencies.  
Built using **Python**, **Flask**, and **SQLAlchemy**.

## ✨ Features

- Add new clients (POST /clients)
- Retrieve a list of all clients (GET /clients)
- SQLite database backend (`crm.db`)
- RESTful API architecture
- Modular project structure using Blueprints
- Ready for future expansion (adding Trips, Projects, etc.)

## 🚀 Technologies Used

- **Python 3.11**
- **Flask** (micro web framework)
- **Flask-SQLAlchemy** (ORM)
- **SQLite** (local database)
- **Postman** (API testing)

## 🗂️ Project Structure
```bash
mini-travel-crm-python-flask/ │ 
    ├── app.py 
    ├── config.py 
    ├── requirements.txt 
    ├── README.md 
    ├── .gitignore │ 
    ├── models/ 
    │   └── client.py │ 
    ├── routes/ 
    │   └── clients.py │ 
    ├── static/ 
    ├── templates/
```

## 📋 How to Run the Project

**1. Clone the repository:**

   ```bash
   git clone https://github.com/naen8918/mini-travel-crm-python-flask.git
   cd mini-travel-crm-python-flask
    

**2. Create and activate virtual environment:**

   
   python -m venv venv
   .\venv\Scripts\activate
   

**3. Install the required dependencies:**

   
   pip install -r requirements.txt
    

**4. Run the Flask app:**

   
   $env:FLASK_APP="app"
   flask run
    ```

**5. The server will start on:**

   (http://127.0.0.1:5000)

**6. Use Postman to test the API:**

   - (POST /clients to add a new client)
   - (GET /clients to list all clients)
