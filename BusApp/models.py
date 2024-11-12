from sqlalchemy import Column, Integer, String, Date, ForeignKey, REAL
from sqlalchemy.orm import relationship
from BusTicketSales.BusApp import db, app
from datetime import datetime

class KhachHang(db.Model):
    __tablename__ = 'KhachHang'
    idKhachHang = Column(Integer, primary_key=True, autoincrement=True)
    hoKhach = Column(String(50), nullable=False)
    tenKhach = Column(String(20), nullable=False)
    soDienThoai = Column(String(255), nullable=False)
    gioiTinh = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    ngaySinh = Column(Date, nullable=False)
    nganHang = Column(String(100), nullable=True)
    soTaiKhoan = Column(String(20), nullable=True)

class NhanVien(db.Model):
    __tablename__ = 'NhanVien'
    idNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    hoNV = Column(String(50), nullable=False)
    tenNV = Column(String(20), nullable=False)
    soDienThoai = Column(String(255), nullable=False)
    gioiTinh = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    ngaySinh = Column(Date, nullable=False)
    nganHang = Column(String(100), nullable=True)
    soTaiKhoan = Column(String(20), nullable=True)

class TuyenXe(db.Model):
     __tablename__ = 'TuyenDuong'
     idTuyenDuong = Column(Integer, primary_key=True, autoincrement=True)
     diemDi = Column(String(50), nullable=False)
     diemDen = Column(String(20), nullable=False)
     khoangCach = Column(REAL, nullable=False)

class Xe(db.Model):
    __tablename__ = 'Xe'
    idXe = Column(Integer, primary_key=True, autoincrement=True)
    bienSo = Column(String(50), nullable=False)
    sucChua = Column(Integer, nullable=False)
    tinhTrangXe = Column(String(20), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()