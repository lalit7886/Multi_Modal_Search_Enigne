from sqlalchemy import create_engine, text

data_base_url = "postgresql://postgres:Unknown%4075@localhost:5432/crawller"

engine = create_engine(data_base_url)

with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    for row in result:
        print(row)
