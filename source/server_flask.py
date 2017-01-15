import os
os.environ["NC_ASSESSMENT_CONFIGURATION"] = "development"
from server import app


app.run(host="0.0.0.0")
