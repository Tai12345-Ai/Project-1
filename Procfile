# Procfile for Heroku, Railway, Render
# Tells platform how to start the app

web: gunicorn --chdir rsa_tool --bind 0.0.0.0:$PORT app_simple:app --workers 2 --timeout 120
