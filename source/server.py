import os
from assessment import create_app


app = create_app(os.getenv("NC_CONFIGURATION"))
