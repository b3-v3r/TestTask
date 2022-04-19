from sqlalchemy import Column, Boolean, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base   
from sqlalchemy.orm import relationship    
from sqlalchemy.orm import sessionmaker  

engine = create_engine('sqlite:///app/main.db')
  
Base = declarative_base()
Base.metadata.bind = engine  

DBSession = sessionmaker(bind=engine)
session = DBSession()


class Payment(Base):  
    __tablename__ = 'payments'
    
    id = Column(String, primary_key=True, unique=True)
    amount = Column( Integer )
    currency = Column( String )
    desciption = Column( String )


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session.commit()
