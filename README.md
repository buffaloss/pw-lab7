# Wander Whirl

## Installation

1. Setup virtual environment (first time only):
```bash
python3 -m venv venv
```

2. Start virtual environment
```bash
# Start virtual environment (linux):
source venv/bin/activate
```

```bash
# Start virtual environment (windows):
venv\Scripts\Activate.ps1
```

3. Install dependencies (first time only):
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
python3 main.py
```

5. Access the documentation at http://localhost:5000/api/swagger

## Notes

.env file is required for the server to run. It should contain the following:
```
JWT_SECRET=<jwt_secret_key>
USERNAME=<username>
PASSWORD=<password>
```
