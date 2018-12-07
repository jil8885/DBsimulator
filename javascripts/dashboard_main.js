employees = document.getElementsByClassName("tooltiptext");
const mariadb = require("mysql");
const async = require("async");
const connection = mariadb.createConnection({host: 'localhost', user: 'root', password: 'a981212', database: 'hotel'});
connection.connect();
const mongodb = require("mongodb").MongoClient;
const dburl = 'mongodb://localhost:27017';
const db = 'hotel';
async.parallel([
    function (next) {
        first();
    },
    function (next) {
        second();
    }
])

function first() {
    for(let i = 1; i <= 15; i++){
        let res = "";
        mongodb.connect(dburl, { useNewUrlParser: true }, function (err, client) {
            const database = client.db("hotel");
            let result = database.collection("employee_position");
            result.find().toArray(function (err, docs) {
                for(let j = 0; j < docs.length; j++){
                    if(docs[j]["position"] === i){
                        connection.query("select name from employee_information where id = " + docs[j]["id"], function (err, rows, fields) {
                            res += "직원 : " + rows[0]["name"] + "<br>";
                        })
                    }
                }
                setTimeout(function () {
                    employees[i - 1].innerHTML = res;
                }, 2000);
                // employees[i - 1].innerHTML = txt;

            });
        });
    }
}

function second() {
    const python = require('python-shell');
    let options = {mode: 'text', pythonPath: '', pythonOptions: ['-u'], scriptPath: '', args: []};
    python.PythonShell.run('/Users/jil8885/WebstormProjects/DBsimulator/sql_update.py', options, function (err, results){});
    setTimeout(function () {
        second();
    }, 1000);
}