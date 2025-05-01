# Mini Travel CRM (Python Flask Project)

This project is a minimal CRM (Customer Relationship Management) system designed for small travel agencies.  
Built using **Python**, **Flask**, and **SQLAlchemy**.

---

## ✨ Features

- Add new clients (`POST /clients`)
- Retrieve a list of all clients (`GET /clients`)
- Create trips linked to clients (`POST /trips`)
- Create invoices for trips (`POST /invoices`)
- View invoices per trip (`GET /invoices/<trip_id>`)
- Record payments for invoices (`POST /payments`)
- View payments per invoice (`GET /payments/<invoice_id>`)
- SQLite database backend (`crm.db`)
- RESTful API architecture
- Modular project structure using Blueprints
- Ready for future expansion (Trips, Projects, etc.)

---

## 🚀 Technologies Used

- **Python 3.11**
- **Flask** (micro web framework)
- **Flask-SQLAlchemy** (ORM)
- **SQLite** (local embedded database)
- **Postman** (API testing)

---

## 🗂️ Project Structure

```bash
mini-travel-crm-python-flask/ │ 
├── app.py # Main Flask application
├── config.py # Database configuration
├── requirements.txt # Dependencies 
├── README.md # Project documentation 
├── .gitignore # Git ignored files │ 
├── models/ # SQLAlchemy models 
│ ├── client.py 
│ ├── trip.py 
│ ├── invoice.py 
│ └── payment.py │ 
├── routes/ # API route blueprints 
│ ├── clients.py 
│ ├── trips.py 
│ ├── invoices.py 
│ └── payments.py │ 
├── static/ # Static files (empty for now) └── templates/ # HTML templates (empty for now)
```


---

## 🧪 API Usage Examples

### 📌 Add a New Client

**POST** `/clients`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123456789",
  "company": "Global Travels"
}
```

### 📌 Create a Trip

**POST** `/trips`
```json
{
  "destination": "Paris",
  "start_date": "2025-06-01",
  "end_date": "2025-06-07",
  "price": 1200.00,
  "notes": "Flight and hotel included",
  "client_id": 1
}
```

### 📌 Create an Invoice
**POST** `/invoices`
```json
{
  "trip_id": 1,
  "issue_date": "2025-06-01",
  "due_date": "2025-06-15",
  "amount": 1200.00,
  "status": "Pending"
}
```

### 📌 Get Invoices for a Trip
**GET** `/invoices/1`

## 📌 Record a Payment
**POST** `/payments`

{
  "invoice_id": 1,
  "payment_date": "2025-06-10",
  "amount": 1200.00,
  "payment_method": "Credit Card"
}
## 📌 Get Payments for an Invoice
**GET** `/payments/1`


## 📋 How to Run the Project

**1. Clone the repository:**

   ```bash
   git clone https://github.com/naen8918/mini-travel-crm-python-flask.git
   cd mini-travel-crm-python-flask
   ```

**1. Create and activate virtual environment:**

   ```
   python -m venv venv
   .\venv\Scripts\activate     # For Windows
   ``` 

**3. Install the required dependencies:**

   ```
   pip install -r requirements.txt
   ```

**4. Run the Flask app:**
   ```
   $env:FLASK_APP="app"
   flask run
   ```

**5. The server will start on:**
    ```
   (http://127.0.0.1:5000)
    ```
**6. Use Postman to test the API:**
    ```
   - (POST /clients to add a new client)
   - (GET /clients to list all clients)
   
   ```

## 👤 Author

- Nazgul Engvall – System Developer with a backend focus

- Built during professional portfolio development to demonstrate backend system architecture