import json, hashlib
from banve.models import *
from banve import db
from flask_login import current_user
from sqlalchemy import func, extract
from datetime import *


def read_country():
    countrys = Airport.query

    return countrys.group_by('country').all()


def read_city():
    city = Airport.query

    return city.all()


def read_list_seat(id=None):
    s = Seat.query

    return s.filter(Seat.idFly == id).all()


def get_id_airport(name=None):
    idair = Airport.query.filter(Airport.city == name)
    if idair.all()==[]:
        return ""
    else:
        return idair.first().id


def get_seat(id=None):
    return Plane.query.filter(Plane.id == id).first().seats


def read_seat(id=None):
    idplane = Flight.query.filter(id == Flight.id).first().idPlane
    return Plane.query.filter(idplane == Plane.id).first().seats


def read_fly(id=None):
    fly = Flight.query
    return fly.get(id)


def get_userid(name=None):
    u = NormalUser.query
    return u.filter(NormalUser.username == name).first().id


def check_c_login(username, password, role=UserRole.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = NormalUser.query.filter(NormalUser.username == username,
                             NormalUser.password == password)
    if user.all()==[]:
        return True
    else:
        return False

def check_login(username,password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = ManagerUser.query.filter(ManagerUser.username == username,
                                    ManagerUser.password == password,
                                    ManagerUser.active == 1).first()
    return user


def read_user_by_cmnd(cmnd=None):
    user = User.query
    user = user.filter(User.idNumber == cmnd).first()
    return user


def read_user(id=None):
    user = db.session.query(User,Phone).with_entities(User.name, User.idNumber, Phone.number).filter(User.id == id, User.id == Phone.idUser).first()
    return user


def get_seats(id=None):
    return Seat.query.filter(Seat.idFly == id).all()


def read_phone(id=None):
    return Phone.query.filter(Phone.idUser == id).first().number


def get_route(idf=None,idt=None):
    try:
      return Route.query.filter(idf==Route.idFrom, idt==Route.idTo).first().id
    except:
        return False


def get_route_fly(idf=None):
    return Flight.query.get(idf).idRoute



def find_flight(airfrom=None,airto=None,datestart=None,dateend=None,seats=None):
    flights = Flight.query
    idfrom = get_id_airport(airfrom)
    idto = get_id_airport(airto)
    route = get_route(idfrom,idto)
    if route == False :
        return False
    else:
        flights = flights.filter(Flight.idRoute == route, datestart <= Flight.day, dateend >= Flight.day)
    return flights.all()


def read_stopport(id = None):
    st = db.session.query(StopPort,Airport).with_entities(Airport.id, Airport.country, Airport.city, StopPort.stopTime, StopPort.note).\
        filter(StopPort.idFly == id, Airport.id == StopPort.idAirport).all()
    return st


def get_price(route=None,c=None):
    return PriceTable.query.filter(c == PriceTable.classes, route == PriceTable.idRoute).first().price



def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + 1
            route = get_route_fly(p["idfly"])
            price = get_price(route,p["classes"])
            total_amount = total_amount + price

    return total_quantity, total_amount


def total(cart):
    total= 0
    if cart:
        for p in cart.values():
            route = get_route_fly(p["idfly"])
            price = get_price(route,p["classes"])
            total = total + price

    return total
def get_airfromto(id):
    fr = Route.query.filter(id == Route.id).all().airfrom
    to = Route.query.filter(id == Route.id).all().to
    return fr , to

def get_u_id(cmnd):
    return User.query.filter(User.idNumber == cmnd).first().id


def createu(cmnd,name,birth,sex,phone):
    birth = datetime.strptime(birth, '%Y-%m-%d').date()
    u = User(name=name,idNumber=cmnd, birth=birth, sex=sex)
    db.session.add(u)
    db.session.commit()
    id = get_u_id(cmnd)
    p = Phone(id = id,number=phone)
    db.session.add(p)
    db.session.commit()


def createu_account(cmnd,name,birth,sex,phone,email,ava,username,password):
    birth = datetime.strptime(birth, '%Y-%m-%d').date()
    try:
        u = User(name=name,idNumber=cmnd, birth=birth, sex=sex)
        db.session.add(u)
        db.session.commit()

        id = get_u_id(cmnd)
        p = Phone(idUser = id,number=phone)
        db.session.add(p)
        db.session.commit()

        a = NormalUser(username=username,password=password,avatar=ava,email=email,id=id)
        db.session.add(a)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def update_seat(seatid,flyid):
    s = Seat.query.filter(Seat.idFly==flyid, Seat.id==seatid).first()
    s.active = 0
    db.session.add(s)
    db.session.commit()


def create_ticket(classes,idseat,idfly,idUser,price,status):

    t = Ticket(classes=classes,idSeat=idseat,idFly=idfly,idCustomer=idUser,price=price,status=status)
    db.session.add(t)
    db.session.commit()


def update_ticket(id):
    t = Ticket.query.get(id)
    t.status = 1;
    db.session.add(t)
    db.session.commit()


def delete_ticket(id):
    t = Ticket.query.get(id)
    s = Seat.query.filter(Seat.idFly == t.idFly, Seat.id == id).first()
    s.active=0
    db.session.add(s)
    db.session.delete(t)
    db.session.commit()


def update_payment(cmnd):
    user = db.session.query(User,Ticket,Route,Flight).with_entities(Route.idFrom,Route.idTo,Flight.id,Ticket.classes,Ticket.idSeat,Ticket.price,Ticket.status,Ticket.id).\
        filter(User.idNumber==cmnd,User.id == Ticket.idCustomer,Ticket.idFly==Flight.id,Flight.idRoute==Route.id).all()
    return user


def baocaothang(m):
    m = datetime.strptime(m, '%Y-%m').date()
    fly = Flight
    for f in fly.query.all():
        s = str(f.day)
        s = s[0:7]
        f.day = datetime.strptime(s, '%Y-%m').date()
    final = db.session.query(fly,Ticket).with_entities(fly.id,func.sum(fly.id),func.sum(Ticket.price)).filter(Ticket.idFly == fly.id,fly.day==m).group_by(fly.id).all()
    s = 0
    for f in final:
        s = f[2] + s
    return final, s

def baocaonam(m):
    m = datetime.strptime(m, '%Y').date()
    fly = Flight
    for f in fly.query.all():
        s = str(f.day)
        s = s[0:4]
        f.day = datetime.strptime(s, '%Y').date()
    final = db.session.query(fly,Ticket).with_entities(fly.id,func.sum(fly.id),func.sum(Ticket.price)).filter(Ticket.idFly == fly.id,fly.day==m).group_by(fly.id).all()
    s=0
    for f in final:
        s = f[2]+s
    return final, s