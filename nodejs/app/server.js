const express = require("express");
const bodyParser = require("body-parser");
const connection = require('./mongo');
const expressHandlebars = require('express-handlebars');
const multer = require('multer');
var fs = require('fs');
const urlRouter = require('./routers');
const app = express()
const methodOverride = require('method-override');


app.use(methodOverride('_method'));
app.use( bodyParser.json() );       // to support JSON-encoded bodies

app.use(bodyParser.urlencoded({extended:true}));

app.set('view engine', 'ejs');
app.set('views', './views');

app.use('/', urlRouter);
app.use(express.static(__dirname + '/public'));

app.use(function(err, req, res, next){
    res.locals.message = err.message;
    res.locals.error  = req.app.get('env') === 'development' ? err : {};
    console.log("err @@@@@@@ ", err);
    res.send({data: [], status: 500, msg: err})
})
let modelsPath = './models'
fs.readdirSync(modelsPath).forEach(function (file) {
    if(~file.indexOf('.js')) require(modelsPath + '/' + file);
});
app.listen(3001, '0.0.0.0', function(){
    console.log("server connect on 3001 PORT")
})