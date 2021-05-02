from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import text

# 리모트 DB 접속 정보
postgres_remote = "postgresql://codestates:school@" + \
                  "codestates-school.cvdrkmeamkhj.ap-northeast-2.rds.amazonaws.com/postgres"
# DB 접속 엔진 생성
engine = create_engine(postgres_remote,
                       echo=True,
                       convert_unicode=True)
# DB 세션 관리 객체 생성
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# DB
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.query = db_session.query_property()

for model in Base.classes:
    print(model)

with engine.connect() as connection:
    result = connection.execute(text("select * from student"))
    for row in result:
        print("student_name:", row['name'])

