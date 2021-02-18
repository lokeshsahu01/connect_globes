const mongoose = require('mongoose');
var AutoIncrement = require('mongoose-sequence')(mongoose);


const CollegeInfoSchema = new mongoose.Schema({
    id : {type: Number, unique: true},
    college : { type: mongoose.Schema.Types.ObjectId, ref: 'college' },
    info : { type : String, required : "Required" },
    created_at : {type : Date, default: Date.now },
    updated_at : { type : Date, default: Date.now },
});

CollegeInfoSchema.plugin(AutoIncrement, {id:'collegeinfoschema_id',inc_field: 'id'});

module.exports = mongoose.model('CollegeInfo', CollegeInfoSchema);