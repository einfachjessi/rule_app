To generate own Flask Session Key for local .env use 
```python3 -c "import secrets; print(secrets.token_hex(16))"``` in terminal and store in a .dotenv as FLASK_SECRET_KEY