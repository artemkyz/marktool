from . import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    date = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    gln = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    password = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False,
    )


class Furs(db.Model):
    __tablename__ = 'furs'
    __table_args__ = {'extend_existing': True}
    gln = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )
    gtin = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )
    kiz = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False,
        primary_key=True
    )
    tid = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )
    sgtin = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )
    sgtin_hex = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )


class UserTemp(db.Model):
    __tablename__ = 'temp_users'
    __table_args__ = {'extend_existing': True}
    date = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    gln = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    password = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    token = db.Column(
        db.String(128),
        index=False,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.gln)
