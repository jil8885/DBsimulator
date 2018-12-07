function step1() {
    let step1 = document.getElementById("step1");
    step1.style.fontSize = "15px";
    step1.style.color = "black";
    step1.style.fontWeight = "bold";
    const mariadb = require("mysql");
    const connection = mariadb.createConnection({host: 'localhost', user: 'root', password: 'a981212', database: 'hotel'});
    connection.connect();
    connection.query("select count(room_number) from room_information", function (err, rows, fields) {
        let number = rows[0]["count(room_number)"]
        if(!err && number === 150){
            connection.query("select count(id) from employee_information", function (err, rows, fields){
                number = rows[0]["count(id)"]
                if(!err && number === 50){
                    connection.query("select count(id) from guest_information", function (err, rows, fields){
                        number = rows[0]["count(id)"]
                        if(!err && number === 5000){
                            step1.innerHTML = "MariaDB 검증 완료";
                            step1.style.color = "grey";
                            step1.style.fontWeight = "normal";
                            step1.style.fontSize = "12px";
                            step2()
                        } else if (number !== 5000) {
                            step1.style.color = "red";
                            step1.innerHTML = "회원 수 불일치";
                            return;
                        } else {
                            step1.style.color = "red";
                            step1.innerHTML = err;
                            return;
                        }
                    })
                } else if (number !== 500) {
                    step1.style.color = "red";
                    step1.innerHTML = "직원 수 불일치";
                    return;
                } else {
                    step1.style.color = "red";
                    step1.innerHTML = err;
                    return;
                }
            })
        } else if (number !== 50) {
            step1.style.color = "red";
            step1.innerHTML = "방 갯수 불일치";
            return;
        } else {
            step1.style.color = "red";
            step1.innerHTML = err;
            return;
        }
    })
}


function step2() {
    let step2 = document.getElementById("step2");
    const mongodb = require("mongodb").MongoClient;
    const dburl = 'mongodb://localhost:27017';
    const db = 'hotel';
    step2.style.fontSize = "15px";
    step2.style.color = "black";
    step2.style.fontWeight = "bold";
    mongodb.connect(dburl, { useNewUrlParser: true }, function (err, client) {
        if(err){
            step2.style.color = "red";
            step2.innerHTML = err;
            return;
        }
        const database = client.db(db);
        let result = database.collection("employee_position");
        result.find().toArray(function (err, docs) {
            if(docs.length === 50){
                result = database.collection("room_temperature");
                result.find().toArray(function (err, docs) {
                    if(docs.length === 150){
                        step2.innerHTML = "MongoDB 검증 완료";
                        step2.style.color = "grey";
                        step2.style.fontWeight = "normal";
                        step2.style.fontSize = "12px";
                        step3();
                    } else {
                        step2.style.color = "red";
                        step2.innerHTML = "방 온도 테이블 초기화 실패";
                    }
                });
            } else {
                console.log(docs.length);
                step2.style.color = "red";
                step2.innerHTML = "직원 위치 테이블 초기화 실패";
            }
        });
    })
}

function step3() {
    let step3 = document.getElementById("step3");
    step3.style.fontSize = "15px";
    step3.style.color = "black";
    step3.style.fontWeight = "bold";
    setTimeout(function () {
        window.location.href = "dashboard_main.html"
    }, 3000)
}