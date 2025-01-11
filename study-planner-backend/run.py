from app import create_app, db
from app.DBmodels import User, StudyPlan

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)