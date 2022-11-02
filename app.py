from flask import Flask
from project.main_blueprint import main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(port=5001)
