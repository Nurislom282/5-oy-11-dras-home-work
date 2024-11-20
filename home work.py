import psycopg2
from propertys import dbname,user,password,host,port
conecting = psycopg2.connect(database=dbname,user=user,password=password,host=host,port=port)
cursor = conecting.cursor()

cursor.execute('''
CREATE TABLE categories(
    categories_id SERIAL NOT NULL UNIQUE,
    categories_name VARCHAR(100),
    categories_description TEXT    
);
''')

cursor.execute('''
CREATE TABLE news(
    news_id SERIAL NOT NULL UNIQUE,
    news_title VARCHAR(200) NOT NULL,
    news_content TEXT NOT NULL,
    news_published_at TIMESTAMP default CURRENT_TIMESTAMP, 
    news_is_published BOOLEAN,
    category_id INT,
    FOREIGN KEY(category_id) REFERENCES categories(categories_id) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE new_comments(
    comments_id SERIAL NOT NULL UNIQUE,
    comments_author_name VARCHAR(100),
    comments_text TEXT NOT NULL,
    comments_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    news_id INT,
    FOREIGN KEY(news_id) REFERENCES news(news_id) ON DELETE SET NULL
);
''')

cursor.execute('''
ALTER TABLE news ADD COLUMN news_views INTEGER DEFAULT 0;
ALTER TABLE new_comments ALTER COLUMN comments_author_name TYPE TEXT;
''',
conecting.commit())

cursor.execute('''
INSERT INTO categories (categories_name,categories_description)
VALUES
('Closes','kiyimlar'),
('Electroniks','telefon planshetlar bor'),
('House holdes','uy hijoslar');

INSERT INTO news (category_id,news_title,news_content,news_published_at,news_is_published)
VALUES
    (1, 'LONDON TRAVEL', 'god', CURRENT_TIMESTAMP, TRUE),
    (2, 'BEGINDER STREET', 'bed', CURRENT_TIMESTAMP, TRUE),
    (3, 'ENSHTEYN BURN', 'very  bad', CURRENT_TIMESTAMP, TRUE);


INSERT INTO new_comments(news_id, comments_author_name,comments_text,comments_created_at)
VALUES
    (1, 'VALI', 'bed', CURRENT_TIMESTAMP),
    (2, 'ISFAANDIYOR', 'good', CURRENT_TIMESTAMP),
    (3, 'MUHAMMADZOHID', 'good', CURRENT_TIMESTAMP);
''',conecting.commit())

cursor.execute('''
UPDATE news
SET views = views + 1;
UPDATE news
SET is_published = TRUE
WHERE published_at < CURRENT_DATE - INTERVAL '1 day';
''',conecting.commit())
cursor.execute('''
DELETE FROM comments
WHERE created_at < CURRENT_DATE - INTERVAL '1 year';
''',conecting.commit())

cursor.execute('''
SELECT 
    news.news_id AS news_id, 
    news.news_title AS news_title, 
    categories.category_name AS category_name
FROM 
    news
INNER JOIN 
    categories ON news.category_id = categories.category_id;
    
    SELECT 
    news.news_id, 
    news.news_title, 
    news.news_content, 
    news.news_published_at
FROM 
    news
INNER JOIN 
    categories ON news.category_id = categories.category_id
WHERE 
    categories.category_name = 'Technology';
    
    SELECT 
    news_id, 
    news_title, 
    news_published_at
FROM 
    news
WHERE 
    news_is_published = TRUE
ORDER BY 
    news_published_at DESC
LIMIT 5;

SELECT 
    news_id, 
    news_title, 
    news_views
FROM 
    news
WHERE 
    news_views BETWEEN 10 AND 100;
    
    SELECT 
    comments_id, 
    comments_author_name, 
    comments_text
FROM 
    new_comments
WHERE 
    comments_author_name LIKE 'A%';
    
    SELECT 
    comments_id, 
    comments_author_name, 
    comments_text
FROM 
    new_comments
WHERE 
    comments_author_name IS NULL;
    
    SELECT 
    categories.category_name AS category_name, 
    COUNT(news.news_id) AS news_count
FROM 
    categories
LEFT JOIN 
    news ON categories.category_id = news.category_id
GROUP BY 
    categories.category_name;
''',cursor.fetchall())

cursor.execute(
    '''
    ALTER TABLE news
ADD CONSTRAINT unique_title UNIQUE (news_title);
    ''',
conecting.commit())



