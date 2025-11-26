# API Documentation

## Base URL

- Development: `http://localhost:8000/api/v1/`
- Production: `https://yourdomain.com/api/v1/`

## Project Name

This is the API documentation for **Eduak Backend** - An E-learning platform.

## Interactive Documentation

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`
- OpenAPI Schema: `/schema/`

## Authentication

The API uses JWT (JSON Web Token) authentication.

### Getting Tokens

1. Register a new account
2. Verify email with OTP
3. Login to receive access and refresh tokens

### Using Tokens

Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Token Refresh

When the access token expires, use the refresh token to get a new one.

## Rate Limiting

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

## Endpoints Overview

### Accounts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/accounts/register/` | Register new user | No |
| POST | `/accounts/otp/send/` | Send OTP to email | No |
| POST | `/accounts/otp/verify/` | Verify OTP and login | No |
| GET | `/accounts/profile/` | Get user profile | Yes |
| PUT | `/accounts/profile/update/` | Update user profile | Yes |
| PUT | `/accounts/password/change/` | Change password | Yes |
| GET | `/accounts/google/login/` | Google OAuth login | No |

### Courses (Public)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/courses/subjects/` | List all subjects | No |
| GET | `/courses/subjects/{slug}/` | Get subject with courses | No |
| GET | `/courses/` | List all courses | No |
| GET | `/courses/{id}/` | Get course details | No |

### Teachers

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/teachers/courses/create/` | Create new course | Yes (Teacher) |
| GET | `/teachers/courses/` | List teacher's courses | Yes (Teacher) |
| GET | `/teachers/courses/{id}/` | Get course details | Yes (Owner) |
| PUT | `/teachers/courses/{id}/update/` | Update course | Yes (Owner) |
| DELETE | `/teachers/courses/{id}/delete/` | Delete course | Yes (Owner) |

### Students

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/students/courses/{id}/enroll/` | Enroll in course | Yes (Student) |
| GET | `/students/courses/enrolled/` | List enrolled courses | Yes (Student) |

## Detailed Endpoints

### 1. User Registration

**POST** `/accounts/register/`

Register a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123456789",
  "role": "student",
  "password": "securepass123",
  "confirm_password": "securepass123"
}
```

**Response (201):**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123456789",
  "role": "student"
}
```

**Notes:**
- Phone is required for teachers
- Password must be at least 8 characters
- Account is inactive until email is verified

---

### 2. Send OTP

**POST** `/accounts/otp/send/`

Send OTP code to user's email for verification.

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response (200):**
```json
{
  "message": "OTP sent successfully."
}
```

---

### 3. Verify OTP

**POST** `/accounts/otp/verify/`

Verify OTP and receive authentication tokens.

**Request Body:**
```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response (200):**
```json
{
  "message": "OTP verified successfully.",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. Get User Profile

**GET** `/accounts/profile/`

Get authenticated user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123456789",
  "role": "student",
  "photo": "/media/profile_pics/photo.jpg",
  "bio": "Student at XYZ University"
}
```

---

### 5. Update User Profile

**PUT** `/accounts/profile/update/`

Update user profile information.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
name: John Updated
phone: 987654321
bio: Updated bio
photo: [file]
```

**Response (200):**
```json
{
  "name": "John Updated",
  "email": "john@example.com",
  "phone": "987654321",
  "role": "student",
  "photo": "/media/profile_pics/new_photo.jpg",
  "bio": "Updated bio"
}
```

---

### 6. Change Password

**PUT** `/accounts/password/change/`

Change user password.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass123",
  "confirm_password": "newpass123"
}
```

**Response (200):**
```json
{
  "message": "Password changed successfully."
}
```

---

### 7. List Subjects

**GET** `/courses/subjects/`

Get list of all subjects with pagination.

**Query Parameters:**
- `limit` (optional): Number of results per page
- `offset` (optional): Starting position

**Response (200):**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/v1/courses/subjects/?limit=10&offset=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Programming",
      "slug": "programming",
      "photo": "/media/courses/subjects/photos/2024/11/24/photo.jpg",
      "total_courses": 15
    }
  ]
}
```

---

### 8. Get Subject Courses

**GET** `/courses/subjects/{slug}/`

Get subject details with all its courses.

**Response (200):**
```json
{
  "subject": "Programming",
  "courses": [
    {
      "id": 1,
      "title": "Python for Beginners",
      "overview": "Learn Python from scratch",
      "owner": "Jane Teacher",
      "photo": "/media/courses/courses/photos/2024/11/24/course.jpg",
      "total_students": 50,
      "total_modules": 10
    }
  ]
}
```

---

### 9. List Courses

**GET** `/courses/`

Get paginated list of all courses with filtering and search.

**Query Parameters:**
- `size` (optional): Results per page (default: 10, max: 50)
- `index` (optional): Starting position
- `search` (optional): Search in title and overview
- `subject__slug` (optional): Filter by subject slug
- `owner__name` (optional): Filter by teacher name
- `ordering` (optional): Sort by field (e.g., `-created`, `title`)

**Response (200):**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/courses/?size=10&index=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python for Beginners",
      "overview": "Learn Python from scratch",
      "subject": {
        "id": 1,
        "title": "Programming",
        "slug": "programming"
      },
      "owner": {
        "id": 1,
        "name": "Jane Teacher",
        "email": "jane@example.com"
      },
      "created": "2024-11-24T10:00:00Z",
      "photo": "/media/courses/courses/photos/2024/11/24/course.jpg",
      "total_students": 50,
      "total_modules": 10
    }
  ]
}
```

---

### 10. Get Course Details

**GET** `/courses/{id}/`

Get detailed information about a specific course.

**Response (200):**
```json
{
  "id": 1,
  "title": "Python for Beginners",
  "overview": "Learn Python from scratch",
  "subject": {
    "id": 1,
    "title": "Programming",
    "slug": "programming"
  },
  "owner": {
    "id": 1,
    "name": "Jane Teacher",
    "email": "jane@example.com"
  },
  "created": "2024-11-24T10:00:00Z",
  "photo": "/media/courses/courses/photos/2024/11/24/course.jpg",
  "total_students": 50,
  "total_modules": 10,
  "modules": [
    {
      "id": 1,
      "title": "Introduction",
      "description": "Getting started with Python",
      "order": 0
    }
  ]
}
```

---

### 11. Create Course (Teacher)

**POST** `/teachers/courses/create/`

Create a new course (teachers only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
title: Python for Beginners
overview: Learn Python from scratch
subject: 1
photo: [file]
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Python for Beginners",
  "overview": "Learn Python from scratch",
  "subject": 1,
  "photo": "/media/courses/courses/photos/2024/11/24/course.jpg"
}
```

---

### 12. List Teacher's Courses

**GET** `/teachers/courses/`

Get list of courses created by authenticated teacher.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Python for Beginners",
    "overview": "Learn Python from scratch",
    "subject": 1,
    "photo": "/media/courses/courses/photos/2024/11/24/course.jpg",
    "total_students": 50,
    "total_modules": 10
  }
]
```

---

### 13. Update Course (Teacher)

**PUT** `/teachers/courses/{id}/update/`

Update course information (owner only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
title: Python Advanced
overview: Advanced Python concepts
subject: 1
photo: [file]
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Python Advanced",
  "overview": "Advanced Python concepts",
  "subject": 1,
  "photo": "/media/courses/courses/photos/2024/11/24/new_course.jpg"
}
```

---

### 14. Delete Course (Teacher)

**DELETE** `/teachers/courses/{id}/delete/`

Delete a course (owner only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204):**
No content

---

### 15. Enroll in Course (Student)

**POST** `/students/courses/{id}/enroll/`

Enroll in a course.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "detail": "You have enrolled in this course"
}
```

**Error Responses:**
- 400: Already enrolled
- 400: Cannot enroll in own course

---

### 16. List Enrolled Courses (Student)

**GET** `/students/courses/enrolled/`

Get list of courses the student is enrolled in.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python for Beginners",
      "overview": "Learn Python from scratch",
      "owner": "Jane Teacher",
      "photo": "/media/courses/courses/photos/2024/11/24/course.jpg"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 429 Too Many Requests
```json
{
  "detail": "Request was throttled. Expected available in X seconds."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

## Best Practices

1. **Always use HTTPS in production**
2. **Store tokens securely** (not in localStorage for web apps)
3. **Refresh tokens before they expire**
4. **Handle rate limiting gracefully**
5. **Validate data on client side before sending**
6. **Use appropriate HTTP methods**
7. **Handle errors properly**
8. **Implement retry logic for failed requests**

## Support

For issues or questions:
- GitHub Issues: https://github.com/akfaqih3/eduak-backend/issues
- Email: support@eduak.com
