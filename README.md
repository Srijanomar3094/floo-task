# Lost & Found API

This is a Django-based Lost & Found API that allows users to report lost and found items and match them after user registration/login.



### 1️⃣ Clone the Repository
```sh
git clone <floo-task>
cd <floo-task>
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv  # For Windows
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` File
Create a `.env` file in the root directory and add your database credentials.

#### MySQL Configuration:
```ini
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306  # Default MySQL port
```

### 5️⃣ Apply Migrations
```sh
python manage.py migrate
```

### 6️⃣ Run the Server
```sh
python manage.py runserver
```

### 7️⃣ Test the API
Use Postman, cURL, or any API testing tool to test the following endpoints:



#### ➤ User Registration (POST)
```sh
POST http://localhost:8000/users/register/
```

#### ➤ User Login (POST)
```sh
POST http://localhost:8000/users/login/
``` 
#### ➤ Report Lost Items (POST)
```sh
POST http://localhost:8000/lost-items/
```
#### ➤ Report Found Items (POST)
```sh
POST http://localhost:8000/found-items/
```

### 8️⃣ Run Tests
```sh
python manage.py test
```


