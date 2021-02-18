const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/testDB',{ useNewUrlParser: true, useUnifiedTopology: true }, (err) => {
    if (!err)
    {
        console.log("success");
    } else {
        console.log("error connecting to database !!!");
    }
})

require('./models/schema');
require('./models/foreignkey');
require('./models/collegeinfo');