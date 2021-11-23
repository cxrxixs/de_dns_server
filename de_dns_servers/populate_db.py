import json
import os
from pathlib import Path
import datetime
import dotenv
import environ
from sqlalchemy import Column, DateTime, Integer, String, create_engine, Boolean, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent

# load environment variables from .env
dotenv_file = os.path.join(BASE_DIR, "jpd_test/.env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

    env = environ.Env(
        # set casting, default value
        DEBUG=(bool, False)
    )
    # reading .env file
    environ.Env.read_env()
    DATABASE_NAME = env('DATABASE_NAME')
    DATABASE_PASSWORD = env('DATABASE_PASSWORD')
    DATABASE_USER = env('DATABASE_USER')
    DATABASE_HOST = env('DATABASE_HOST')



# Database connection
engine = create_engine(f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}")
S = sessionmaker()
S.configure(bind=engine)
session = S()


# Database model
Base = declarative_base()

class DNSServer(Base):
    __tablename__ = "de_dns_servers"

    # id = models.AutoField(primary_key=True)
    id = Column(Integer, primary_key=True)

    # ip_address = models.GenericIPAddressField(null=False)
    ip_address = Column(String)

    # name = models.CharField(max_length=100, null=True)
    name = Column(String(100), nullable=True)

    # as_number = models.IntegerField(null=False)
    as_number = Column(Integer)

    # as_org = models.CharField(max_length=256, null=False)
    as_org = Column(String(256))

    # country_code = models.CharField(max_length=10, null=True)
    country_code = Column(String(10), nullable=True)

    # city = models.CharField(max_length=100, null=True)
    city = Column(String(100), nullable=True)

    # version = models.CharField(max_length=512, null=True)
    version = Column(String(512), nullable=True)

    # error = models.BooleanField(default=False, null=True)
    # Raw data is not boolean type but empty string, need to convert
    error = Column(Boolean, default=False, nullable=True)

    # dnssec = models.BooleanField(null=True)
    dnssec = Column(Boolean, nullable=True)

    # reliability = models.DecimalField(max_digits=3, decimal_places=2)
    reliability = Column(Float)

    # checked_at = models.IntegerField(null=True)
    # Insert year only, convert from ISO to datetime
    checked_at = Column(Integer, nullable=True)

    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = Column(DateTime)


# Read dns raw data from json file
with open("dns_raw_data.json") as infile:
    data = json.load(infile)


# loop to all data and insert to database
for dns in data:
    record = DNSServer(
        ip_address=dns["ip"],
        name=dns["name"],
        as_number=dns["as_number"],
        as_org=dns["as_org"],
        country_code=dns["country_id"],
        city=dns["city"],
        version=dns["version"],
        error=False if dns["error"] == "" else True,
        dnssec=dns["dnssec"],
        reliability=dns["reliability"],
        checked_at=datetime.datetime.fromisoformat(dns["checked_at"].split(".")[0]).year,
        created_at=dns["created_at"]
    )


    session.add(record)
    session.commit()
