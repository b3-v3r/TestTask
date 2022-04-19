import sys
from app.main import app
from app.models_db import session, engine, Base
import os

if __name__ == "__main__":

    try:
        Base.metadata.create_all(engine)
        session.commit()
    except:
        pass

    os.chdir("app/")
    app.run()
