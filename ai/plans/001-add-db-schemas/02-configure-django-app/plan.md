# Task 02: Configure Django App

## Overview

Register the `productivity_core` app in Django settings so that Django recognizes it and can use its models, migrations, and other features.

## Type

Code changes only

## Files to Modify

### 1. `productivity_app/productivity_app/settings.py`

**Current state:**
- INSTALLED_APPS list contains 6 default Django apps (lines 33-40):
  - django.contrib.admin
  - django.contrib.auth
  - django.contrib.contenttypes
  - django.contrib.sessions
  - django.contrib.messages
  - django.contrib.staticfiles

**Required change:**
- Add `'productivity_core',` to the INSTALLED_APPS list after the default Django apps

**Implementation details:**
- Insert the new app entry after `'django.contrib.staticfiles',` (line 39)
- Add it as a new line before the closing bracket
- Follow the existing formatting pattern (indentation with 4 spaces, trailing comma)
- The app name should be exactly `'productivity_core',` (with quotes and trailing comma)

**Expected result:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'productivity_core',
]
```

## Notes

- This change is required before running migrations in task 04
- Django must know about the app to discover its models and create database tables
- The app name matches the directory name created in task 01 (`productivity_core/`)
- No other configuration is needed for Django to recognize the app

## Validation

After making this change, you can verify it worked by:
1. Running `python manage.py check` (should show no errors)
2. Running `python manage.py diffsettings | grep productivity_core` (should show the app in INSTALLED_APPS)

However, these validation steps are optional and not part of this task.
