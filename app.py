import os
from codestates_school import create_app
# 앱 생성
app = create_app()
postgres_remote = "postgresql://codestates:school@" + \
                  "codestates-school.cvdrkmeamkhj.ap-northeast-2.rds.amazonaws.com/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_remote
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
