import pymysql
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from ..config.settings import DB_CONFIG

def upload_to_database(yawn, blink):
    try:
        # Get current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create a dataframe with the new data
        data = {'시간': [current_time], '눈감음': [blink], '하품': [yawn]}
        df = pd.DataFrame(data)

        # Create SQLAlchemy engine
        engine = create_engine(
            f'mysql+pymysql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}/{DB_CONFIG["db"]}'
        )

        # Upload processed data to database
        df.to_sql(name='pi03_data', con=engine, if_exists='append', index=False)
        print("Data uploaded successfully")
        
    except Exception as e:
        print(f"Database upload error: {e}")