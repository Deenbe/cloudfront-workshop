const express = require("express");
const app = express();

app.get('/api', (req, res) => {
    console.log(JSON.stringify(req.headers))
    if (req.query.info) {
      require('child_process').exec('cat '+ req.query.info,
        function (err, data) {
          res.send(new Date().toISOString() + '\n' + JSON.stringify(req.headers)+ '\n'+data)
        });
    } else {
      res.send(new Date().toISOString() + '\n' + JSON.stringify(req.headers))
    }
});
app.get("/apireqheaders", (req, res) => {
    console.log("/apireqheaders called ");
    console.log(JSON.stringify(req.headers))
    res.send(new Date().toISOString() + '\n' + JSON.stringify(req.headers))
});
app.get("/apiquerystring", (req, res) => {
    console.log("/apiquerystring called ");
    console.log(req.query)
    res.send(new Date().toISOString() + '\n' + JSON.stringify(req.query))
});
app.listen(3000, () => {
    console.log("Server running on port 3000");
});
