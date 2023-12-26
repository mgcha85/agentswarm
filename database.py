from datetime import datetime
from sqlalchemy import create_engine
import psycopg2


class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        # DB 연결 설정
        DB_HOST = "localhost"
        DB_PORT = 5432
        DB_USER = "mingyu"
        DB_PASS = "alsrb2091"
        DB_NAME = "loud_sourcing"

        # SQLAlchemy 엔진 생성
        self.engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # psycopg2 연결
        self.conn = psycopg2.connect(
            host=DB_HOST, 
            port=DB_PORT, 
            user=DB_USER, 
            password=DB_PASS, 
            dbname=DB_NAME
        )
        self.cursor = self.conn.cursor()

    def string_escape(self, str):
        return str.replace("'", "''")
    
    def disconnect(self):
        # psycopg2 연결 종료
        if self.conn:
            self.conn.close()
        # SQLAlchemy 엔진 연결 종료
        if self.engine:
            self.engine.dispose()

    def create_table(self):
        # naver_search 테이블 생성
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS naver_search (
                id SERIAL PRIMARY KEY,
                text TEXT,
                images TEXT,
                title TEXT,
                link TEXT,
                bloggername TEXT,
                postdate DATE
            )
        ''')

    def insert_by_series(self, tname, data):
        columns = ', '.join(data.index)
        values = ", ".join(["%s"] * data.shape[0])

        # 데이터 삽입
        sql = f'''
        INSERT INTO {tname} ({columns})
        VALUES ({values})
        '''
        self.cursor.execute(sql, tuple(data.values))
        self.conn.commit()

    def insert_data(self, data):
        # 문자열 형태의 날짜를 datetime 객체로 변환
        postdate = datetime.strptime(data['postdate'], '%Y%m%d')

        # 데이터 삽입
        self.cursor.execute('''
        INSERT INTO naver_search (text, images, title, link, topic, bloggername, postdate)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['text'], ';'.join(data['images']), data['title'], data['link'], data['topic'], data['bloggername'], postdate))
        self.conn.commit()
