const mongoose = require('mongoose');
var AutoIncrement = require('mongoose-sequence')(mongoose);

const collegeSchema = new mongoose.Schema({
    id : {type: Number, unique: true},
    email : { type : String, required : "Required" },
    username : { type : String, required : "Required" },
    full_name : { type : String, required : "Required" },
    logoimage: { type : String, default:''},
    collegeimage: { type : String, default:''},
    bannarimage: { type : String, default:''},
    brochurefile: { type : String, default:''},
    collegegallary: { type : Array, default:[]},
    created_at : {type : Date, default: Date.now },
    updated_at : { type : Date, default: Date.now },

});

collegeSchema.plugin(AutoIncrement, {id:'collegeSchema_id',inc_field: 'id'});
module.exports = mongoose.model('college', collegeSchema);


