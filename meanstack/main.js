class calculator{
    constructor(a, b){
        this.a = a;
        this.b = b
    }
    add(c){
        this.c = c;
        return this.a + this.b + this.c;
    }
    minus(d){
        this.d = d;
        return this.a - this.b - this.c - this.d ;
    }
    multi(e){
        this.e = e;
        return this.a * this.b * this.c * this.d * this.e;
    }
    divid(f){
        this.f = f;
        return this.a / this.b / this.c / this.d / this.e / this.f;
    }
}


module.exports.s = calculator;