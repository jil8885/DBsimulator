const mariadb = require("mysql");
const connection = mariadb.createConnection({host: 'localhost', user: 'root', password: 'a981212', database: 'hotel'});
connection.connect();
window.onload = function () {
    execute(floor)
};

function execute(floor) {
    check_reservation(floor);
    setTimeout(function () {
        execute(floor);
    }, 500);
}

function check_reservation(floor) {
    connection.query("select state_transaction, state_in_room from room_information where floor=" + floor, function (err, rows, fields) {
        let rooms = document.getElementsByClassName("room");
        for(let i = 0; i < rooms.length; i++){
            if(rows[i]["state_transaction"] === 0)
                rooms[i].style.backgroundColor = "white";
            else if(rows[i]["state_transaction"] === 1){
                if(rows[i]["state_in_room"] === 0)
                    rooms[i].style.backgroundColor = "pink";
                else if(rows[i]["state_in_room"] === 1)
                    rooms[i].style.backgroundColor = "red";
            }
        }
    })
}
