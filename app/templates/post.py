class Movie(db.Model):
    __tablename__ = 'movies'  # creating a table name
    __table_args__ = (
        CheckConstraint('Date < Current_Date',)
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), unique=True)
    year = db.Column(db.Date, nullable=False)
    genre = db.Column(db.String(80), nullable=False)

