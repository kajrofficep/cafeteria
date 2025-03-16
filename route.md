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
```markdown
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "john_doe", "password": "securepassword123"}'
```
```markdown
curl http://127.0.0.1:5000/protected
```

```markdown
curl -X POST http://127.0.0.1:5000/logout
```

```markdown
curl http://127.0.0.1:5000/admin
curl http://127.0.0.1:5000/moderator
```

```markdown
curl http://127.0.0.1:5000/profile
```

```markdown
curl -X PUT http://127.0.0.1:5000/profile/update \
-H "Content-Type: application/json" \
-d '{"full_name": "Updated Name", "email": "updated@example.com"}'
```

curl -X PUT http://127.0.0.1:5000/profile \
-H "Content-Type: application/json" \
-d '{"new_password": "new_secure_password"}'

```markdown
curl http://127.0.0.1:5000/admin/profile/2

```

```markdown
http://127.0.0.1:5000/admin/users
```

```markdown
http://127.0.0.1:5000/meals
```