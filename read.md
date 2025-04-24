## ⚙️ Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** and add your PostgreSQL settings:
```env
DB_NAME=yourdbname
DB_USER=yourdbuser
DB_PASSWORD=yourdbpassword
DB_HOST=localhost
DB_PORT=5432
```

5. **Apply migrations**
```bash
python manage.py migrate
```

6. **Create a superuser**
```bash
python manage.py createsuperuser
```

8. **Add existing forms**
```bash
python manage.py 
```

7. **Run the development server**
```bash
python manage.py feed_existing_forms
```

Now visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to view the project.
