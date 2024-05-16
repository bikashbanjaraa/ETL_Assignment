import psycopg2

#connect to posgresql

conn = psycopg2.connect(
    dbname="",
    user="",
    password="",
    host="localhost"
)

# Create a cursor object
cur = conn.cursor()


# Define SQL CREATE TABLE statement
create_table_query = """
CREATE TABLE youtube_data (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    views INTEGER,
    likes INTEGER,
    dislikes INTEGER
);
"""

# Execute the CREATE TABLE statement
cur.execute(create_table_query)
conn.commit()

# Load data into the PostgreSQL table
for row in scraped_data:
    insert_query = """
    INSERT INTO youtube_data (video_id, title, description, views, likes, dislikes)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    cur.execute(insert_query, (row['video_id'], row['title'], row['description'], row['views'], row['likes'], row['dislikes']))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()