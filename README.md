# Cadee — Personal Finance Tracker

Cadee is a personal finance tracker built around a “folder stack” interface: instead of switching between pages for history, limits, and analysis, the app keeps everything in one stacked space and lets the user surface the most important layer with a tap. The visual goal is “predictive calm,” so the UI leans on warm neutrals, soft shadows, and rounded folder tabs to reduce money anxiety and keep the dashboard approachable.

The dashboard is the heart of the project. It combines live transaction data, weekly/monthly limits, analytics summaries, and purchase goals in a single view. The content is driven by Django models, so as soon as a user adds a transaction or goal, the UI updates automatically. That feedback loop is what makes the design feel like a companion rather than a static display.

This project was built to show a blend of backend and frontend complexity: custom data entry flows (transactions, limits, and goals) are wired into Django views and forms, while the UI uses a layered animation technique to simulate folder stacking. The result is a cohesive product experience rather than a collection of separate pages.

## Distinctiveness and Complexity

This project is distinct because it does not follow the common “finance dashboard = charts + tables” pattern. The core interaction is the folder stack, which keeps multiple financial contexts (history, limits, and analysis/goals) present at the same time. That required a custom layout and interaction model rather than the default multi-page CRUD approach, and it changes how users navigate the product: they “surface” information instead of switching sections.

The complexity comes from connecting this UI concept to live data. Transactions, limits, and goals are stored in separate models and are aggregated into month and week summaries, percentages, and progress ratios. Those values are computed in the view layer and displayed in different cards, so a single change can impact multiple parts of the UI. The app also supports dynamic profile updates, avatar uploads, and goal status badges, which adds state management complexity across templates.

Another layer of complexity is the cohesive design system across multiple experiences: dashboard, add/edit forms, login/register, and profile settings share the same visual language (type, spacing, buttons, shadows) but serve different purposes. This requires careful CSS architecture so the UI remains consistent while still feeling polished and intentional on both desktop and mobile.

## Files and What They Contain

- `Cadee/manage.py`: Django management entry point.
- `Cadee/cadee_core/settings.py`: Project settings, installed apps, static/media config, login redirects.
- `Cadee/cadee_core/urls.py`: Routes for dashboard, auth, transactions, limits, goals, profile, and media (debug).
- `Cadee/cadee_core/wsgi.py` and `Cadee/cadee_core/asgi.py`: Server entry points.
- `Cadee/finance/models.py`: Data models for profiles, categories, transactions, purchase goals, and budget limits.
- `Cadee/finance/views.py`: Dashboard logic, CRUD flows for transactions/goals/limits/profile, auth views.
- `Cadee/finance/forms.py`: Model forms for transactions, limits, goals, profile, plus auth forms.
- `Cadee/finance/admin.py`: Admin registration and display config for finance models.
- `Cadee/finance/apps.py`: App config for the finance app.
- `Cadee/finance/tests.py`: Placeholder for tests.
- `Cadee/finance/migrations/0001_initial.py`: Initial schema.
- `Cadee/finance/migrations/0002_alter_transaction_date.py`: Enables editable transaction dates.
- `Cadee/finance/migrations/0003_userprofile_profile_image.py`: Adds profile avatar support.
- `Cadee/finance/migrations/0004_create_default_user.py`: Creates default user `Marti / 12345`.
- `Cadee/templates/finance/base.html`: Base template with fonts and CSS include.
- `Cadee/templates/finance/dashboard.html`: Main dashboard layout and folder stack logic.
- `Cadee/templates/finance/add_transaction.html`: Transaction creation form.
- `Cadee/templates/finance/transactions_list.html`: Full transaction history list.
- `Cadee/templates/finance/edit_limits.html`: Weekly/monthly limit update form.
- `Cadee/templates/finance/add_goal.html`: Purchase goal creation form.
- `Cadee/templates/finance/update_goal.html`: Goal progress update form.
- `Cadee/templates/finance/edit_profile.html`: Profile edit (name + avatar).
- `Cadee/templates/finance/login.html`: Login screen.
- `Cadee/templates/finance/register.html`: Registration screen.
- `Cadee/static/css/styles.css`: Global styling, dashboard layout, and auth UI.
- `Cadee/static/assets/cadee_corgi.svg`: Cadee logo used on auth screens and fallback avatars.
- `Cadee/db.sqlite3`: SQLite database for local development.

## How to Run

1) Create and activate a virtual environment, then install dependencies (Django).
2) Run migrations:
```
python manage.py migrate
```
3) Start the server:
```
python manage.py runserver
```
4) Visit the app at `http://127.0.0.1:8000/`.

Default account (created via migration):
- Username: `Marti`
- Password: `12345`

## Additional Notes

- Uploaded images (profile/goal images) are stored under `media/` in development.
- Auth pages are functional but designed as a front-end first experience; additional password reset flows can be added later.
- If you want to use a custom PNG logo, drop it into `Cadee/static/assets/` and update the template references.
