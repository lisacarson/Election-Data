from firebase import firebase

class Database:
    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://election-data-2ad46.firebaseio.com', None)

    def get(self, key):
        self.firebase.get(key)

    def set(self, key, val):
        self.firebase.post(key, val)


if __name__ == "__main__":
    db = Database()
    db.set('bar', 'foo')
