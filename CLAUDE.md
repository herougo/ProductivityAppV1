# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a productivity tracking application built with Django (backend) and vanilla JavaScript (frontend). The project emphasizes learning Django, exploring vanilla JavaScript best practices, and creating a functional productivity tracker.

## Architecture

### Frontend Structure

The frontend uses a **page-based architecture** where Webpack dynamically discovers pages:

1. **Page discovery:** Webpack scans `src/html/pages/*.html` files
2. **For each page, it looks for:**
   - HTML template: `src/html/pages/{page}.html` (required)
   - JavaScript entry: `src/js/pages/{page}/main.js` (optional)
   - Page styles: `src/css/3-bem/pages/{page}.css` (optional)

3. **CSS layering** (loaded in this order):
   - `1-global/` - Base styles and colors
   - `2-early-utility/` - Early utility classes
   - `3-bem/pages/` - Page-specific BEM styles
   - `4-custom-bootstrap/` - Custom Bootstrap overrides
   - `5-late-utility/` - Late utility classes (highest specificity)

**To add a new page:**
1. Create `src/html/pages/newpage.html`
2. Optionally create `src/js/pages/newpage/main.js`
3. Optionally create `src/css/3-bem/pages/newpage.css`
4. Run webpack build - the page is auto-discovered

**Output:**
- Built files go to `frontend/dist/`
- CSS: `dist/css/[name].[contenthash].css`
- JS: `dist/js/[name].[contenthash].js`
- HTML: `dist/{page}.html`

### Backend Structure

Currently a vanilla Django 6.0.2 project with:
- SQLite database
- No custom Django apps yet (only default contrib apps)
- Settings in `productivity_app/productivity_app/settings.py`
- Root URLconf in `productivity_app/productivity_app/urls.py`

**Note:** When creating Django apps, use `python manage.py startapp {appname}` from the `productivity_app/` directory.

## Key Configuration Files

- `requirements.txt` - Python dependencies (Django 6.0.2)
- `productivity_app/frontend/package.json` - Node dependencies and build scripts
- `productivity_app/frontend/webpack.config.js` - Webpack configuration with dynamic page discovery
- `productivity_app/productivity_app/settings.py` - Django settings

## Development Notes

- The project uses **Django 6.0.2** (latest as of project creation)
- Frontend uses **vanilla JavaScript** (no frameworks) - avoid suggesting React, Vue, etc.
- Webpack config has dynamic page discovery logic - be careful when modifying it
- CSS architecture follows a layered approach for specificity management
- The `ai/` directory contains documentation, plans, and prompts for AI assistance
