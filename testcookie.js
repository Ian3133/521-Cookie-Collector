const https = require('https');
const sqlite3 = require('sqlite3').verbose();

function printList(list) {
    for (let i=0; i<list.length; i++) {
        console.log(list[i]);
    }
}

function sendCookies(domain, cookies) {

    let options = {
        host: domain,
        method: 'GET',
        path: '/',
        headers: {'Cookie': cookies}
    };

    let req = https.request(options, function(res) {
        console.log('Status: ' + res.statusCode);
        console.log('Headers: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log('Body: ' + chunk);
            //if body contains the term "redirect", then you're logged in
        });
    });

    req.on('error', function(e) {
        console.log('Problem with request: ' + e.message);
    });

    req.end();
}

let db = new sqlite3.Database('./Cookies', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        return console.error(err.message);
    }
    console.log('Connected to the database.');
});

let cookies = [];
let query = `SELECT * FROM cookies WHERE host_key LIKE '%piazza%'`;

db.serialize(() => {
    db.each(query, (err, row) => {
        if (err) {
            console.error(err.message);
        }
        cookies.push(row.name + "=" + row.value);
    });
});

sendCookies('piazza.com', cookies);

db.close((err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Close the database connection.');
});
