username = 'postgres'
password = 'cognitiveati'
host = 'telle-ai-database.cqh3eh5shl0r.us-east-2.rds.amazonaws.com'
port = 5432
test_db = 'telle_ai_dev'

db_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, test_db)

mail_settings = {
    "MAIL_SERVER": 'smtp.zoho.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": 'noreply@telle.ai',
    "MAIL_PASSWORD": 'blissmotors'
}

ipinfo_access_token = '362e2dc65c9e7a'
