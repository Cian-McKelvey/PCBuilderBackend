from dotenv import load_dotenv
import os

load_dotenv()  # Loading environment variables

# The thought behind using the constants file to load the environment variables is to act as a store
# so that they only fetch the values once here, instead of everytime one is required

# MongoDB's connection information
MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")
STAGING_DATABASE = os.getenv("STAGING_DATABASE")
PRODUCTION_DATABASE = os.getenv("PRODUCTION_DATABASE")
BUILDS_COLLECTION = os.getenv("BUILDS_COLLECTION")
BUILDS_INDEX_COLLECTION = os.getenv("BUILDS_INDEX_COLLECTION")
USER_COLLECTION = os.getenv("USER_COLLECTION")
BLACKLIST_COLLECTION = os.getenv("BLACKLIST_COLLECTION")

# Flask's config
SECRET_KEY = os.getenv("SECRET_KEY")

# Relational connection information
RELATIONAL_DATABASE_URL = os.getenv("RELATIONAL_DATABASE_URL")
RELATIONAL_TABLE_NAME = os.getenv("RELATIONAL_TABLE_NAME")

# Functional Args
PART_COST_RANGE = 25  # Outlines the range of part price e.g. x-20% -> x+20%
