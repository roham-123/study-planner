from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

# Extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()  # Initialize Migrate globally

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import models after db initialization
    with app.app_context():
        from app.DBmodels import User, StudyPlan

    # Register blueprints
    from app.routes.auth import auth
    from app.routes.study_plan import study_plan
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(study_plan, url_prefix='/api')

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        return str(identity)  # Simply convert the identity (user.id) to a string

    return app