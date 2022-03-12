import random, string

def generate_string(length=16):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def shorten_url(db, url, URL):
    url = URL(url, generate_string(16))
    db.session.add(url)
    db.session.commit()
    return url