var k = require("./main");

var z = new k.s(2, 4);
console.log(z.add(6));
console.log(z.minus(8));
console.log(z.multi(10));
console.log(z.divid(12));

var St = function(){
    this.name = 'lokesh';
    this.age = 25;
    this.email = 'as@as.com';
}

St.prototype = {
    address: "jaipur",
    getName: function() {
        return this.name
    }
}

var st_obj = new St();
console.log(st_obj.getName());