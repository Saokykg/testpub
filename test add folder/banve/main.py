from flask import render_template, request, \
    redirect, session, jsonify
from datetime import date
from banve import app, utils, decorator
from banve import *
from banve.models import *
from banve.admin import  *
from datetime import date
from flask_login import login_user, logout_user
import os, json, hashlib


@app.route('/')
def index():
    logout_user()
    session['page']={}
    # del session['user']
    if 'user' not in session:
        session['user']={
            "username":"",
            "id":""
        }
    d = str(date.today())
    session['cart'] = {}
    session['search'] = {
        "airfrom" : "",
        "airto": "",
        "seats" : "",
        "datestart": d,
        "dateend" : d,
    }
    countrys = utils.read_country()
    citys = utils.read_city()
    d = date.today()
    return render_template('index.html',info = session['search'], countrys=countrys, citys=citys,date=d)


@app.route('/search1')
def tosearch():
    info = session['search']
    countrys = utils.read_country()
    citys = utils.read_city()
    return render_template('search.html',info = info,countrys=countrys, citys=citys,kt = False,fly="")


# search.html
@app.route('/search2')
def search():
    s = session['search']
    countrys = utils.read_country()
    citys = utils.read_city()
    airfrom = request.args.get('airfrom')
    airto = request.args.get('airto')
    seats =request.args.get('seats')
    datestart = request.args.get('datestart')
    dateend=request.args.get('dateend')
    s={
        "airfrom" : airfrom,
        "airto": airto,
        "seats" : seats,
        "datestart": datestart,
        "dateend" : dateend,
    }
    if s['datestart'] == "" or s['datestart'] ==None:
        s['datestart'] = str(date.today())
    if s['dateend'] == "" or s['dateend'] ==None:
        s['dateend']= str(date.today())
    session['search'] = s
    flights = utils.find_flight(airfrom=airfrom,airto=airto,datestart=s['datestart'],dateend=s['dateend'],seats=seats)
    if flights == False:
        kt = True
    else:
        kt = False
    return render_template('search.html',info=s,countrys=countrys, citys=citys,fly=flights,kt = kt)


@app.route('/searchb')
def backsearch():
    s = session['search']
    countrys = utils.read_country()
    citys = utils.read_city()
    if s['airfrom'] != None and s['airto'] != None:
        flights = utils.find_flight(airfrom=s['airfrom'], airto=s['airto'], datestart=s['datestart'], dateend=s['dateend'], seats=s['seats'])
        if flights == []:
            flights = ""
    else:
        flights = ""
    return render_template('search.html', info=s, countrys=countrys, citys=citys, fly=flights)



@app.route('/getinfo', methods=['post'])
def getinfo():
    data = json.loads(request.data)
    id = str(data.get("id"))
    s = utils.read_list_seat(id=id)
    return s



# book.html
@app.route('/book/<int:idfly>')
def book(idfly):
    seats = utils.read_list_seat(id = idfly)
    seat = utils.read_seat(id=idfly)
    fly = utils.read_fly(id=idfly)
    stopport = utils.read_stopport(id=idfly)
    if stopport == []:
        kt=False
    else:
        kt=True
    return render_template('book.html',seats=seats,seat=seat,fly=fly,info=session['search'],st=stopport,kt=kt)


@app.route('/api/cart', methods=['post'])
def cart():
    cart = session['cart']

    data = json.loads(request.data)
    idseat = str(data.get("idseat"))
    idfly = str(data.get("idfly"))
    classes = str(data.get("classes"))
    route = utils.get_route_fly(idfly)
    price = utils.get_price(route, classes)
    if idseat in cart:
        cart.pop(idseat)
    else:
        cart[idseat] = {
            "idseat": idseat,
            "idfly": idfly,
            "classes": classes,
            "price": price
        }
    session['cart'] = cart

    quan, price = utils.cart_stats(cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan
    })


@app.route('/logincostumer',methods=['post','get'])
def loginc():
    if session['user']['username']!="":
        return render_template('logincostumer.html',kt=True)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        if username == None or username == "":
            kt=False
        else:
            user = utils.check_c_login(username=username, password=password)
            if user==True:
                kt=False
            else:
                s =session['user']
                s['username'] = username
                s['id'] = utils.get_userid(name=username)
                session['use'] = s
                kt=True
    else:
        kt = False
    return render_template('logincostumer.html',kt=kt)


@app.route('/api/pay', methods=['post'])
def pay():
    if session['cart'] == {}:
        return jsonify({'message': 'Chưa chọn ghế!','err':0})
    data = json.loads(request.data)
    idfly = str(data.get("idfly"))
    u = session['user']
    if u['username'] == "":
        return jsonify({'message': 'Đăng nhập để đặt vé!!','err':1})
    else:
        return jsonify({'message': 'ok'})




# payment.html
@app.route('/payment')
def payment():
    s =session['search']
    u = session['user']
    if (u['id']!=""):
        user = utils.read_user(u['id'])
        kt=True
    else:
        kt=False
        user = "";
    sum = utils.total(session['cart'])
    return render_template('payment.html',s=s,u=u,user=user,sum=sum,kt=kt)



@app.route('/api/logout',methods=['post'])
def logout():
    s = session['user']
    s['username']= ""
    s['id'] = ""
    session['user']=s
    return jsonify({'mes' : 'logout'})


@app.route('/api/logincostume',methods=['post'])
def logincostume():
    data = json.loads(request.data)
    page = str(data.get("page"))
    p = session['page']
    p = page
    session['page'] = p
    return jsonify()


@app.route('/api/info',methods=['post'])
def getinfouser():
    data = json.loads(request.data)
    cmnd = str(data.get("cmnd"))
    user = utils.read_user_by_cmnd(cmnd)
    if user==None:
        return jsonify({'message': 'Chưa có thông tin trong hệ thống \n yêu cầu nhập thêm thông tin!!!','stt':0})
    else:
        phone = utils.read_phone(user.id)
        b= str(user.birth)
        return jsonify({'name' : user.name, 'birth' : b, 'sex': user.sex, 'phone': phone, 'stt':1})


@app.route('/api/createuser',methods=['post'])
def createuser():
    data = json.loads(request.data)
    cmnd = str(data.get("cmnd"))

    user = utils.read_user_by_cmnd(cmnd)
    if user==None:
        birth = data.get("birth")
        name = str(data.get("name"))
        sex = str(data.get("sex"))
        phone = str(data.get("phone"))

        utils.createu(cmnd,name,birth,sex,phone)
    id = utils.get_u_id(cmnd)
    # user = utils.read_user(id)
    u = session['user']
    u['id']=id
    session['user']=u
    return jsonify({'message': '!!!'})



@app.route('/api/booked',methods=['post'])
def booked():
    data = json.loads(request.data)
    kt = data.get("kt")
    cart = session['cart']
    u = session['user']
    for c in cart.values():
        cl = int(c['classes'])
        ids = int(c['idseat'])
        idf = int(c['idfly'])
        idu = u['id']
        price = c['price']
        utils.create_ticket(classes=cl,idseat=ids,idfly=idf,idUser=idu,price=price,status=kt)
        utils.update_seat(seatid=ids,flyid=idf)
    if u['id']=="" or u['username']=="":
        u['id']=""
        u['username'] = ""
    session['user']=u
    return jsonify({'message': 'Đặt vé thành công!!!'})


# safety.html
@app.route('/safety')
def safety():
    return render_template('safety.html')


# contacts.html
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/manager')
def manager():
    if current_user.is_authenticated:
        return render_template('manager.html')
    else:
        return redirect('/admin')


@app.route('/baocao')
def baocao():
    if current_user.is_authenticated:
        bct = request.args.get("baocaothang")
        bcn = request.args.get("baocaonam")
        s=None
        if bct:
            baocaothang, s = utils.baocaothang(m=bct)
        else:
            baocaothang = None
        if bcn:
            baocaonam, s = utils.baocaonam(m=bcn)
        else:
            baocaonam = None
        return render_template('baocao.html',bct=baocaothang,bcn=baocaonam,s=s)
    else:
        return redirect('/admin')



@app.route('/tracuu')
def tracuu():
    return render_template('manager.html')



@app.route('/thanhtoan')
def thanhtoan():
    if current_user.is_authenticated:
        cmnd = request.args.get("cmnd")
        ticket = utils.update_payment(cmnd)
        if ticket:
            city = utils.read_city()
            return render_template('ThanhToan.html',ticket=ticket,city=city)
        else:
            return render_template('ThanhToan.html',ticket=None)
    else:
        return redirect('/admin')


@app.route('/api/thanhtoan',methods=['post'])
def apithanhtoan():
    data = json.loads(request.data)
    id = data.get("id")
    utils.update_ticket(id=id)
    return jsonify({'message': 'hành công!!!'})


@app.route('/api/xoave',methods=['post'])
def apixoave():
    data = json.loads(request.data)
    id = data.get("id")
    utils.delete_ticket(id=id)
    return jsonify({'message': 'thành công!!!'})




@app.route('/login', methods=['post'])
def login_usr():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

    return redirect('/admin')


@login.user_loader
def user_load(user_id):
    return ManagerUser.query.get(user_id)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password == confirm:
            name = request.form.get('name')
            birth = request.values.get('birth')
            sex = request.values.get('sex')
            cmnd = request.values.get('cmnd')
            sdt = request.values.get('phone')
            email = request.form.get('email')
            username = request.form.get('username')
            avatar = request.files["avatar"]
            avatar_path = 'images/upload/%s' % avatar.filename
            # avatar.save(os.path.join(app.root_path,
            #                              'static/',
            #                              avatar_path))
            if utils.createu_account(cmnd=cmnd,name=name,birth=birth,sex=sex,phone=sdt,email=email,ava=avatar_path,username=username,password=password):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)




if __name__ == '__main__':
    app.run(debug=True)
