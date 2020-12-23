function  addseat(e, idseat, idfly, classes){
    if (e.classList.contains("chosen"))
        e.classList.remove("chosen")
    else
        e.classList.add("chosen");
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "idseat": idseat,
            "idfly": idfly,
            "classes": classes
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        var cart = document.getElementById("total");
        var c = document.getElementById("countseat")
        c.innerText = `${data.total_quantity}`;
        cart.innerText = `${data.total_amount} VNĐ`;
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}
function pay(idfly){
    fetch('/api/pay', {
        method: "post",
        body: JSON.stringify({
            "idfly": idfly,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        if (data.err == 1)
            location.href = '/logincostumer';
        else
            location.href = '/payment';
    }).catch(err => {
        console.log(err);
    })
}

function logout(){
    fetch('/api/logout', {
        method: "post",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.mes);
        location.href = window.location.pathname;
    }).catch(err => {
        console.log(err);
    })
}

function logincostume(){
     fetch('/api/logincostume', {
        method: "post",
        body: JSON.stringify({
            "page": window.location.pathname,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        location.href='/logincostumer'
    }).catch(err => {
        console.log(err);
    })
}

function getinfo(){
    cmnd = document.getElementById("idNumber").value;
    fetch('/api/info', {
        method: "post",
        body: JSON.stringify({
            "cmnd": cmnd,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.stt == 0)
            alert(data.message);
        else{
            document.getElementById("name").value = data.name;
            document.getElementById("birth").value = data.birth;
            document.getElementById(data.sex).checked = true;
            document.getElementById("phone").value = data.phone;
        }
    }).catch(err => {
        console.log(err);
    })
}
function createuser(){
    cmnd = document.getElementById("idNumber").value;
    name = document.getElementById("name").value
    birth = document.getElementById("birth").value
    phone = document.getElementById("phone").value
    if (document.getElementById("Nam").checked = true)
        sex = document.getElementById("Nam").value
    else
        sex = document.getElementById("Nu").value
    fetch('/api/createuser', {
        method: "post",
        body: JSON.stringify({
            "cmnd": cmnd,
            "name": name,
            "birth":birth,
            "sex":sex,
            "phone":phone
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(window.location.pathname);
        location.href = window.location.pathname;
    }).catch(err => {
        console.log(err);
    })
}

function book(kt){
    fetch('/api/booked', {
        method: "post",
        body: JSON.stringify({
            "kt": kt
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        location.href = '/'
    }).catch(err => {
        console.log(err);
    })
}
function thanhtoan(id){
    fetch('/api/thanhtoan', {
        method: "post",
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert("da thanh toan");
        var s = "tt" + id
        alert(s)
        document.getElementById(s).innerText="Đã thanh toán";
    }).catch(err => {
        console.log(err);
    })
}
function xoa(id){
    fetch('/api/xoave', {
        method: "post",
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert("Da xoa");
        var s = "xv" + toString(id)
        document.getElementById(s).innerText="Đã xóa";
    }).catch(err => {
        console.log(err);
    })
}

