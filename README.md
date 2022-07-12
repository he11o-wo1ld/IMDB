# IMDB
Movie


## Create Virtual Environment
### For MAC
```python3 -m venv venv```

### For Windows
'''python -m venv venv'''


## Activate the virtual environment
### For MAC
'''source venv/bin/activate'''

# For Windows
source venv/Scripts/activate

# Install the requirements from the requirements.txt file.
# MAC
pip3 install -r requirements.txt

# Windows
pip install -r requirements.txt

# Start server
uvicorn main:app --reload

# Sweager UI:
http://127.0.0.1:8000/docs
