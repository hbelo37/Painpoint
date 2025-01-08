from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
else:
    application = app  # This line is important for gunicorn