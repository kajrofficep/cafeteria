# Create user
POST /create_user
```markdown
curl -X POST http://127.0.0.1:5000/create_user \
-H "Content-Type: application/json" \
-d '{
    "username": "john_doe",
    "full_name": "John Doe",
    "department": "Engineering",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "password": "securepassword123"
}'
```
# Get user
GET /users
```markdown
curl http://127.0.0.1:5000/users
```