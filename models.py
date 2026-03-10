from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class DonVi(db.Model):
    __tablename__ = 'DonVi'

    IDDonVi = db.Column(db.Integer, primary_key=True)
    TenDonVi = db.Column(db.String(255), nullable=False)
    DiaDiem = db.Column(db.String(255))
    Website = db.Column(db.String(255))
    Email = db.Column(db.String(150))
    DienThoai = db.Column(db.String(50))
    MoTa = db.Column(db.Text)
    IsParent = db.Column(db.Boolean, default=False, nullable=False)
    ParentID = db.Column(db.Integer, db.ForeignKey('DonVi.IDDonVi'), nullable=True)

    parent = db.relationship(
        'DonVi',
        remote_side=[IDDonVi],
        backref=db.backref('children', lazy=True)
    )

class NguoiDung(UserMixin, db.Model):
    __tablename__ = 'NguoiDung'

    IDNguoiDung = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(20), default='admin', nullable=False)

    def get_id(self):
        return str(self.IDNguoiDung)