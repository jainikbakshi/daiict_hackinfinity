<<<<<<< HEAD
from flask_frozen import Freezer
from app import app
import requests

freezer = Freezer(app)

if __name__ == '__main__':
=======
from flask_frozen import Freezer
from myapp import app

freezer = Freezer(app)

if __name__ == '__main__':
>>>>>>> 7ab2b5015469a871916f5c976f6d8f1d112d0a50
	freezer.freeze()