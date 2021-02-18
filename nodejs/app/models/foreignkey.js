const mongoose = require('mongoose');
var AutoIncrement = require('mongoose-sequence')(mongoose);


const ReferenceSchema = new mongoose.Schema({
    id : {type: Number, unique: true},
    college : { type: mongoose.Schema.Types.ObjectId, ref: 'college' },
    height : { type : String, required : "Required" },
    weight : { type : String, required : "Required" },
    created_at : {type : Date, default: Date.now },
    updated_at : { type : Date, default: Date.now },
});

ReferenceSchema.plugin(AutoIncrement, {id:'referencemodel_id',inc_field: 'id'});

module.exports = mongoose.model('refDB', ReferenceSchema);