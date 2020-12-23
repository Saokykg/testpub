from sqlalchemy import Column, Integer, String, Boolean, \
    Enum, Float, ForeignKey, DateTime, Time, Text, Date
from sqlalchemy.orm import relationship
from banve import db
from flask_login import UserMixin
from enum import Enum as UserEnum
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


# Airport
class Airport(Base):
    __tablename__ = 'airport'

    country = Column(String(20), nullable=False)
    city= Column(String(100), nullable=False)

    airport_stop = relationship('StopPort', backref='airport', lazy=True)


# Route
class Route(Base):
    __tablename__ = 'route'

    idFrom = Column(Integer, ForeignKey(Airport.id), nullable=False)
    idTo = Column(Integer, ForeignKey(Airport.id), nullable=False)

    idfromfk = relationship('Airport',foreign_keys=[idFrom])
    idtofk = relationship('Airport',foreign_keys=[idTo])
    route_price = relationship('PriceTable', backref='route', lazy=True)
    route_fly = relationship('Flight', backref='route', lazy=True, uselist=False)


# PriceTable
class PriceTable(Base):
    __tablename__ = 'priceTable'

    idRoute = Column(Integer, ForeignKey(Route.id), nullable=False)
    classes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


# Plane
class Plane(Base):
    __tablename__ = 'plane'

    seats = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    plane_fly = relationship('Flight', backref='plane',lazy=True)
    # plane_seat = relationship('Seat', backref='plane', lazy=True)


# Flight
class Flight(Base):
    __tablename__ = 'flight'

    idPlane = Column(Integer, ForeignKey(Plane.id), nullable=False)
    idRoute = Column(Integer, ForeignKey(Route.id), nullable=False)
    day = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    flyTime = Column(Time, nullable=False)

    fly_stop = relationship('StopPort', backref='flight', lazy=True)
    fly_ticket = relationship('Ticket', backref='flight', lazy=True)
    fly_seat = relationship('Seat', backref='flight', lazy=True)


# stopPort
class StopPort(Base):
    __tablename__ = 'stopPort'

    idFly = Column(Integer, ForeignKey(Flight.id), nullable=False)
    idAirport = Column(Integer, ForeignKey(Airport.id), nullable=False)
    stopTime = Column(Time, nullable=False)
    note = Column(Text, nullable=True)


# Seats
class Seat(Base):
    __tablename__ = 'seat'

    classes = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    idFly = Column(Integer, ForeignKey(Flight.id), primary_key=True, nullable=False)
    seat_fly = relationship('Flight', backref='seat', lazy=True)


# Customer
class User(Base):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    birth = Column(Date)
    idNumber = Column(String(10), nullable=False)
    sex = Column(String(3))

    cus_tick = relationship('Ticket', backref='user', lazy = True)
    nUser = relationship('NormalUser', backref='user', uselist = False)
    sUser = relationship('ManagerUser', backref='user', uselist = False)
    phone_cus = relationship('Phone', backref='user', lazy=True)



# phone
class Phone(db.Model):
    __tablename__ = 'phone'

    idUser = Column(Integer, ForeignKey(User.id), primary_key=True, nullable=False)
    type = Column(String(20), nullable=False, default="Mobile")
    number = Column(String(10), primary_key=True, nullable=False)


# NormalUser
class NormalUser(db.Model):
    __tablename__ = 'normalUser'

    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    email = Column(String(50), nullable=False)
    id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable=False)



class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


# StaffUser
class ManagerUser(db.Model, UserMixin):
    __tablename__ = 'manageruser'

    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    email = Column(String(50), nullable=False)
    id = Column(Integer, ForeignKey(User.id),primary_key=True, nullable=False)

    staff_ticket = relationship('Ticket', backref='staffUser', lazy=True)
    def __str__(self):
        return self.name


# Ticket
class Ticket(Base):
    __tablename__ = 'ticket'

    classes = Column(Integer, nullable=False)
    idSeat = Column(Integer, ForeignKey(Seat.id), nullable=False)
    idFly = Column(Integer, ForeignKey(Flight.id),nullable=False)
    idCustomer = Column(Integer, ForeignKey(User.id), nullable=False)
    price = Column(Float, nullable=False)
    idStaff = Column(Integer,ForeignKey(ManagerUser.id), nullable=True)
    price = Column(Float, nullable=False)
    status = Column(Integer, nullable=False)



# Rules
class Rule(Base):
    __tablename__ = 'rules'

    maxiumAirport = Column(Integer, nullable=False)
    miniumFlyTime = Column(Time, nullable=False)
    maxiumStopPort = Column(Integer, nullable=False)
    miniumStopTime = Column(Time, nullable=False)
    maxiumStopTime = Column(Time, nullable=False)
    miniumBookTime = Column(Time, nullable=False)



if __name__ == '__main__':
    db.create_all()