import psycopg

conn = psycopg.connect(host="localhost", dbname="membership_dashboard", user="postgres", password="qlcthrma53/Pos", port=5433)

cur = conn.cursor()

conn.commit()

cur.close()
conn.close()