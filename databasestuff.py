def setup(db):
    class URL(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        originalurl = db.Column(db.String(256), unique=True, nullable=False)
        shorturl = db.Column(db.String(16), unique=True, nullable=False)
        clicks = db.Column(db.Integer, default=0)
        
        def __init__(self, originalurl, shorturl):
            self.originalurl = originalurl
            self.shorturl = shorturl
            self.clicks = 0
    
    return URL