# Fantasy Football League Manager

Flask + MySQL fantasy football management app.

## Setup

1. Install dependencies: `pip install flask mysql-connector-python python-dotenv`
2. Copy `.env.example` to `.env` and fill in your MySQL credentials
3. Run the schema: `mysql -u root -p < schema.sql`
4. Seed the data: `mysql -u root -p < seed.sql`
5. Run the app: `python app.py`
6. Visit `http://localhost:5000`
