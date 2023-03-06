from app import app, __init__
from dbcreds import production_mode

if (production_mode == True):
    print("Running server in production mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5006)
else:
    print("Running in testing mode")
    from flask_cors import CORS
    CORS(app)
app.run(debug=True)