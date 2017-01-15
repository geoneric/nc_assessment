import os
from nc_assessment import create_app


app = create_app(os.getenv("NC_ASSESSMENT_CONFIGURATION"))
