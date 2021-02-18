const http = require('http')
const server = http.createServer(function(req, res){
    res.write('asdfasdfssssssdfsdf')
    res.end();
}).listen(3000)