
const mongoose = require('mongoose');
const Schema = mongoose.Schema;
var AutoIncrement = require('mongoose-sequence')(mongoose);


let examCategorySchema = new Schema({
    id : {type: Number, default: null, unique: false},
    user: {type: Number, required: "required"},
    updated_by: {type: Number, default: ''},
    Category: {type: String, default: '', unique: true},
    categoryIcon: {type: String, default: ''},
    sub_category: {type: Number, default: null},
    slug: {type: String, default: ''},
    categorybanner: {type: String, default: ''},
    created_at : {type : Date, default: Date.now },
    updated_at : { type : Date, default: Date.now },
})

examCategorySchema.plugin(AutoIncrement, {id:'ExamCategory_id',inc_field: 'id'});
mongoose.model('ExamCategory', examCategorySchema);