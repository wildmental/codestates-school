import os
from flask import Flask
from codestates_school.database import Base, db_session
from flask import render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Settings for development
    app.debug = True
    urls = {'메인 페이지': 'index',
            '학생 관리': 'student',
            '교과목 관리': 'lecture',
            '수강 관리': 'enroll'}

    # root page
    @app.route('/')
    def root():
        return 'This is the root page!'

    # Hello page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/index', methods=['GET'], endpoint='index')
    def show_index():
        return render_template('index.html', urls=urls)

    @app.route('/student', methods=['GET'], endpoint='student')
    def show_students():
        students = Base.classes.student.query.all()
        return render_template('students.html', students=students, urls=urls)

    @app.route('/lecture', methods=['GET'], endpoint='lecture')
    def show_lectures():
        lectures = Base.classes.lecture.query.all()
        return render_template('lectures.html', lectures=lectures, urls=urls)

    @app.route('/enroll', methods=['GET'], endpoint='enroll')
    def show_enrolls():
        enrolls = Base.classes.enroll.query.all()
        return render_template('enrolls.html', enrolls=enrolls, urls=urls)

    # 앱 종료시 DB connection 을 함께 종료
    @app.teardown_appcontext
    def db_session_remove(exception=None):
        db_session.remove()
        print('SQLAlchemy : DB session removed successfully')

    return app
