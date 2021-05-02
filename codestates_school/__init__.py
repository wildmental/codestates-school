import os
from flask import Flask, redirect, url_for, request
from codestates_school.database import Base, db_session
from flask import render_template
from sqlalchemy.orm import joinedload


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
            '개설 교과목 관리': 'lecture',
            '수강 관리': 'enroll_list'}

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
        model = Base.classes.student
        # joined load 는 left outer join 이 기본. (타겟 테이블 조회 시 쿼리 단일화 용도에 적절)
        # inner join 이 필요한 경우 joined load 의 inner join 옵션 지정
        students = db_session.query(model).options(joinedload(model.school),
                                                   joinedload(model.department)).all()
        return render_template('students.html', students=students, urls=urls)

    @app.route('/lecture', methods=['GET'], endpoint='lecture')
    def show_lectures():
        model = Base.classes.lecture
        subject = Base.classes.subject
        room = Base.classes.room
        # 2차 relation 참조 필요합 경우 joined load 체이닝으로 ORM 쿼리 통합
        lectures = db_session.query(model).options(joinedload(model.subject).options(joinedload(subject.department)),
                                                   joinedload(model.room).options(joinedload(room.building)),
                                                   joinedload(model.professor)).all()
        return render_template('lectures.html', lectures=lectures, urls=urls)

    @app.route('/enroll/', methods=['GET'], endpoint='enroll_list')
    def show_enrolls():
        model = Base.classes.enroll
        lecture = Base.classes.lecture
        enrolls = db_session.query(model).order_by(model.id).options(joinedload(model.student),
                                                                     joinedload(model.lecture)
                                                                     .options(joinedload(lecture.subject))).all()
        return render_template('enrolls.html', enrolls=enrolls, urls=urls)

    @app.route('/enroll/form/', methods=['GET'], endpoint='enroll_form')
    def enroll_form():
        model = Base.classes.enroll
        db_session.query(model)
        return render_template('enroll_form.html', urls=urls)

    @app.route('/enroll/', methods=['POST'], endpoint='enroll_create')
    def enroll_create():
        # 학번으로 학생 테이블 pk 가져오기
        student_no = request.form.get("student_no")
        student = Base.classes.student
        student_id = db_session.query(student).filter_by(student_no=student_no).one().id

        # 과목 코드와 학기 정보로 최신 개설강좌 pk 가져오기
        subject_code = request.form.get("subject_code")
        subject = Base.classes.subject
        subject_id = db_session.query(subject).filter_by(code=subject_code).one().id
        semester = request.form.get("semester")
        lecture = Base.classes.lecture
        lecture_id = db_session.query(lecture).filter_by(semester=semester)\
                                              .filter_by(subject_id=subject_id).first()
        grade = request.form.get("grade", None)

        # # enroll 생성 및 저장
        # enroll = Base.classes.enroll(student_id=student_id, lecture_id=lecture_id, grade=grade)
        # created = db_session.add(enroll)
        # db_session.commit()
        return redirect(url_for("enroll_list"))

    @app.route('/enroll/<pk>/update/', methods=['POST'], endpoint='enroll_update')
    def enroll_update(pk):
        grade = request.form.get("grade")
        model = Base.classes.enroll
        db_session.query(model).filter(model.id == pk).update({"grade": grade})
        db_session.commit()
        return redirect(url_for("enroll_list"))

    @app.route('/enroll/<pk>/del/', methods=['GET'], endpoint='enroll_del')
    def enroll_delete(pk):
        model = Base.classes.enroll
        db_session.query(model).filter_by(id=pk).delete()
        db_session.commit()
        return redirect(url_for("enroll_list"))

    # 앱 종료시 DB connection 을 함께 종료
    @app.teardown_appcontext
    def db_session_remove(exception=None):
        db_session.remove()
        print('SQLAlchemy : DB session removed successfully')

    return app
