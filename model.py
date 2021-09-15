from app import db, app
from sqlalchemy.dialects.postgresql import JSON
from dataclasses import dataclass

@dataclass
class RadioStation(db.Model):
    __tablename__ = 'radio_stations'

    id: int
    name: str
    description: str
    logo: str
    category: str
    streamUrl: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    logo = db.Column(db.String())
    category = db.Column(db.String())
    streamUrl = db.Column(db.String())

