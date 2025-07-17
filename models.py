from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# It`s always a good practice to provide this to help sqlalchemy adequately name
# the constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",  # indexing -> for better querying
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # unique
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # ck -> CHECK -> validations CHECK age > 18;
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # foreign key
    "pk": "pk_%(table_name)s",  # primary key
}

# this allows us to define tables and their columns
metadata = MetaData(naming_convention=naming_convention)

# create a db instance
db = SQLAlchemy(metadata=metadata)


class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=True
    )
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())

    # uselist = False -> this indicates a one relationship
    user = db.relationship("User", back_populates="categories", uselist=False)

    # it removes these fields
    serialize_rules = ("-user_id", "-user")


class Entry(db.Model, SerializerMixin):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id", ondelete="cascade"
        ),  # this will delete all user entries if the user is deleted
        nullable=False,
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "categories.id", ondelete="set null"
        ),  # this will not delete the entries but rather just sets the column to NULL
        nullable=True,
    )
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=datetime.now())  # UPDATE
    deleted_at = db.Column(db.TIMESTAMP)  # soft deleting

    user = db.relationship("User", back_populates="entries", uselist=False)


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.VARCHAR, nullable=False, unique=True)
    password = db.Column(db.VARCHAR, nullable=True)
    role = db.Column(
        db.Enum("admin", "user"), nullable=False, server_default="user"
    )  # admin and user
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=datetime.now())

    # define relationships
    categories = db.relationship("Category", back_populates="user")
    entries = db.relationship("Entry", back_populates="user")

    serialize_rules = ("-password", "-categories", "-entries")


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkout_id = db.Column(db.VARCHAR)
    mpesa_code = db.Column(db.VARCHAR)
    paying_phone = db.Column(db.VARCHAR)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())
