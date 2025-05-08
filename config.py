# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_V1_STR: str = os.getenv("API_V1_STR", "/api")
PROJECT_NAME: str = os.getenv("PROJECT_NAME", "VulnScan-Server")

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

STORAGE_BUCKET = "cloud-files"
FILES_TABLE = "files"
PROJECTS_TABLE = "projects"
SCANS_TABLE = "scans"
VULNERABILITIES_TABLE = "vulnerabilities"
USERS_TABLE = "users"

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
