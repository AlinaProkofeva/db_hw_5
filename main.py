
import psycopg2

with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt','r') as file:
    passw = file.read()

conn = psycopg2.connect(database='test_db', user='postgres', password=passw)

with conn.cursor() as cur:
    cur.execute("""
        DROP TABLE homework;
        DROP TABLE course;
    """)

    cur.execute('''
        CREATE TABLE IF NOT EXISTS course (
            id SERIAL PRIMARY KEY,
            name VARCHAR(120) UNIQUE NOT NULL
            );
            ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS homework(
            id SERIAL PRIMARY KEY,
            number INTEGER NOT NULL,
            description TEXT NOT NULL,
            course_id INTEGER NOT NULL REFERENCES course(id)
            );
    ''')

    conn.commit()

    cur.execute('''
        INSERT INTO course (name) VALUES (%s) RETURNING id, name;
        ''', ('Pythooon',))
    print(cur.fetchone())

    cur.execute('''
        INSERT INTO course (name) VALUES ('Java') RETURNING id, name;
        ''')
    print(cur.fetchone())
    print()

    conn.commit()

    cur.execute('''
        SELECT * FROM course;
        ''')
    print(cur.fetchmany(3)[1])

    azzz = str(1)

    cur.execute('''
        SELECT name FROM course
        WHERE id=%s;    
    ''', azzz)
    print(cur.fetchall())

    def get_course_id(cursor, name: str):
        cursor.execute('''
        SELECT id FROM course 
        WHERE name=%s;
        ''', (name,))
        return cur.fetchone()[0]

    print(f"id выбранного курса = {get_course_id(cur, 'Java')} ")

    cur.execute('''
        UPDATE course SET name = %s
        WHERE id = %s;
        ''', ('C+', 2))
    conn.commit()

    cur.execute('''
        SELECT * FROM course
        ''')
    print(cur.fetchall())



conn.close()