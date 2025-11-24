# Migration Guide

This guide explains the database changes and how to apply them.

## Database Changes Summary

### 1. User Model (accounts.User)

**New Indexes Added:**
- `db_index=True` on `name` field
- `db_index=True` on `email` field (already unique)
- `db_index=True` on `role` field
- Composite index on `['email', 'role']`
- Composite index on `['is_active', 'role']`

**Why:** These fields are frequently used in queries and filtering.

### 2. Subject Model (courses.Subject)

**New Indexes Added:**
- `db_index=True` on `title` field
- `db_index=True` on `slug` field (already unique)

**Why:** Used in search and filtering operations.

### 3. Course Model (courses.Course)

**New Indexes Added:**
- `db_index=True` on `owner` ForeignKey
- `db_index=True` on `subject` ForeignKey
- `db_index=True` on `title` field
- `db_index=True` on `created` field
- Composite index on `['subject', '-created']`
- Composite index on `['owner', '-created']`
- Composite index on `['title', '-created']`

**Why:** These fields are used in filtering, sorting, and searching.

## How to Apply Migrations

### Step 1: Backup Your Database

**IMPORTANT:** Always backup before running migrations!

```bash
# For SQLite (development)
cp db.sqlite3 db.sqlite3.backup

# For PostgreSQL (production)
pg_dump -U eduak_user eduak_db > backup_$(date +%Y%m%d).sql
```

### Step 2: Activate Virtual Environment

```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Step 3: Create Migrations

```bash
python manage.py makemigrations
```

Expected output:
```
Migrations for 'accounts':
  accounts/migrations/0002_auto_YYYYMMDD_HHMM.py
    - Alter field name on user
    - Alter field email on user
    - Alter field role on user
    - Add index accounts_user_email_role_idx on field(s) email, role of model user
    - Add index accounts_user_is_active_role_idx on field(s) is_active, role of model user

Migrations for 'courses':
  courses/migrations/0002_auto_YYYYMMDD_HHMM.py
    - Alter field title on subject
    - Alter field slug on subject
    - Alter field owner on course
    - Alter field subject on course
    - Alter field title on course
    - Alter field created on course
    - Add index courses_course_subject_created_idx on field(s) subject, -created of model course
    - Add index courses_course_owner_created_idx on field(s) owner, -created of model course
    - Add index courses_course_title_created_idx on field(s) title, -created of model course
```

### Step 4: Review Migrations

```bash
# View SQL that will be executed
python manage.py sqlmigrate accounts 0002
python manage.py sqlmigrate courses 0002
```

### Step 5: Apply Migrations

```bash
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, courses, sessions, students, teachers
Running migrations:
  Applying accounts.0002_auto_YYYYMMDD_HHMM... OK
  Applying courses.0002_auto_YYYYMMDD_HHMM... OK
```

### Step 6: Verify Migrations

```bash
# Check migration status
python manage.py showmigrations

# Test the application
python manage.py runserver
```

## Rollback Procedure

If something goes wrong:

### Option 1: Rollback Migrations

```bash
# Rollback to previous migration
python manage.py migrate accounts 0001
python manage.py migrate courses 0001
```

### Option 2: Restore from Backup

```bash
# For SQLite
cp db.sqlite3.backup db.sqlite3

# For PostgreSQL
psql -U eduak_user eduak_db < backup_YYYYMMDD.sql
```

## Performance Impact

### During Migration

- **Small databases (<10,000 records):** < 1 minute
- **Medium databases (10,000-100,000 records):** 1-5 minutes
- **Large databases (>100,000 records):** 5-30 minutes

**Note:** Creating indexes on large tables can take time. Plan accordingly.

### After Migration

**Expected improvements:**
- Faster course listing (30-50% improvement)
- Faster user queries (20-40% improvement)
- Faster filtering operations (40-60% improvement)

## Production Deployment

### Recommended Approach

1. **Test in staging environment first**
2. **Schedule maintenance window**
3. **Notify users of downtime**
4. **Backup database**
5. **Apply migrations**
6. **Verify functionality**
7. **Monitor performance**

### Zero-Downtime Migration (Advanced)

For large production databases:

```bash
# 1. Create indexes concurrently (PostgreSQL only)
python manage.py migrate --fake

# 2. Manually create indexes with CONCURRENTLY
psql -U eduak_user eduak_db

CREATE INDEX CONCURRENTLY accounts_user_name_idx ON accounts_user(name);
CREATE INDEX CONCURRENTLY accounts_user_role_idx ON accounts_user(role);
-- ... etc

# 3. Mark migrations as applied
python manage.py migrate --fake
```

## Troubleshooting

### Error: "relation already exists"

**Solution:**
```bash
# Fake the migration
python manage.py migrate --fake accounts 0002
python manage.py migrate --fake courses 0002
```

### Error: "database is locked" (SQLite)

**Solution:**
```bash
# Stop the development server
# Close any database connections
# Try again
python manage.py migrate
```

### Error: "permission denied"

**Solution:**
```bash
# Check database permissions
# For PostgreSQL
GRANT ALL PRIVILEGES ON DATABASE eduak_db TO eduak_user;
```

### Migration takes too long

**Solution:**
```bash
# For PostgreSQL, create indexes concurrently
# See "Zero-Downtime Migration" section above
```

## Verification Queries

After migration, verify indexes were created:

### SQLite

```sql
-- Check indexes
.indexes accounts_user
.indexes courses_course
.indexes courses_subject
```

### PostgreSQL

```sql
-- Check indexes
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename IN ('accounts_user', 'courses_course', 'courses_subject');
```

### Django Shell

```python
python manage.py shell

from django.db import connection
cursor = connection.cursor()

# List all indexes
cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='index' AND tbl_name='accounts_user';
""")
print(cursor.fetchall())
```

## Performance Testing

Before and after migration:

```python
# Test query performance
import time
from courses.models import Course

# Test 1: List courses
start = time.time()
courses = list(Course.objects.select_related('owner', 'subject').all()[:100])
print(f"Time: {time.time() - start:.4f}s")

# Test 2: Filter by subject
start = time.time()
courses = list(Course.objects.filter(subject__slug='programming')[:100])
print(f"Time: {time.time() - start:.4f}s")

# Test 3: Search
start = time.time()
courses = list(Course.objects.filter(title__icontains='python')[:100])
print(f"Time: {time.time() - start:.4f}s")
```

## Next Steps

After successful migration:

1. ✅ Monitor application performance
2. ✅ Check error logs
3. ✅ Verify all features work correctly
4. ✅ Update documentation
5. ✅ Notify team of completion

## Support

If you encounter issues:
- Check logs: `tail -f logs/django.log`
- GitHub Issues: https://github.com/akfaqih3/eduak-backend/issues
- Email: support@eduak.com

## Checklist

- [ ] Database backed up
- [ ] Virtual environment activated
- [ ] Migrations created
- [ ] Migrations reviewed
- [ ] Migrations applied
- [ ] Application tested
- [ ] Performance verified
- [ ] Documentation updated

Good luck with your migration! 🚀
