const express = require("express");
const router = express.Router();
// var fs = require('fs');
const mongoose = require('mongoose');
const dbmodel = mongoose.model('college');
const referencedbmodel = mongoose.model('refDB');
const CollegeInfobModel = mongoose.model('CollegeInfo');
var path = require('path');
const crypto = require('crypto');
const GridFsStorage = require('multer-gridfs-storage');
const Grid = require('gridfs-stream');
const jszip = require('jszip');
const multer = require('multer');

const mongoURI = "mongodb://localhost:27017/testDB";

// connection
const conn = mongoose.createConnection(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

let gfs;
conn.once("open", () => {
  // init stream
  gfs = new mongoose.mongo.GridFSBucket(conn.db, {
    bucketName: "uploads"
  });
});

const storage = new GridFsStorage({
    url: mongoURI,
    file: (req, file) => {
      return new Promise((resolve, reject) => {
        crypto.randomBytes(16, (err, buf) => {
          if (err) {
            return reject(err);
          }
          const filename = file.originalname;
          const fileInfo = {
            filename: filename,
            bucketName: "uploads"
          };
          resolve(fileInfo);
        });
      });
    }
  });

var upload = multer({ storage: storage})

router.get("/image/", (req, res) => {
    // console.log('id', req.params.id)
    const zip = new jszip();
    const file = gfs.find().toArray((err, files) => {
        if (!files || files.length === 0) {
          return res.status(404).json({
            err: "no files exist"
          });
        }
        for(const file of files){
          const p = gfs.openDownloadStreamByName(file.filename);
          const fileChunks = [];
          p.on('data', chunk => { fileChunks.push(chunk) })
          p.on('end', async () => {
            const file = Buffer.concat(fileChunks);
            await zip.file(file.filename, file, { base64: true })
            
          })
        };
        console.log("zip = ", zip);
        zip.generateAsync({ type: "nodebuffer" })
              .then(function (content) {

                  //deliver zip folder to font end
                  res.send(content);
              })
              .catch(err => {
                  next(err)
              });
      });
  });

  router.get('/download', async (req, res, next) => {
    try {
        const lists = [];
        const zip = new jszip();
        let downloaded = 0;

        lists.map(async (item, index) => {
          console.log("index =" ,index);
            let fileName;
            //find name by id from metadata
            await gfs.find().toArray((err, search) => {
                if (err) {
                    console.log(err)
                }
                console.log("search =" ,search);
                console.log(search.filename)
                fileName = search.filename;
            })

            const readStream = gfs.createReadStream({ _id: search._id });

            let fileChunks = [];
            //store all chunks into an array
            readStream.on('data', chunk => { fileChunks.push(chunk) });

            //when all chunks of a files have been read...
            readStream.on('end', async () => {

                //assemble all chunks into a file
                const file = Buffer.concat(fileChunks);
                console.log(file);

                //store file in zip folder
                await zip.file(fileName, file, { base64: true })
                console.log(index)

                //record # of files donwloaded
                downloaded++;

                //when all downloaded files are in zip folder...
                    zip.generateAsync({ type: "nodebuffer" })
                        .then(function (content) {

                            //deliver zip folder to font end
                            res.send(content);
                        })
                        .catch(err => {
                            next(err)
                        });
                
            })
        })


    } catch (err) {
        return next(err)
    }
})

router.get("/filesdownload", (req, res)=>{
  (async() => {
    const downloaded = 0;
    const files = await gfs.find().toArray();
    for(const data of files) {
      console.log("data._id = ", data._id );
      const readStream = gfs.createReadStream({ _id: data._id });
      if(!readStream){
        continue
      }
      let fileChunks = [];
      readStream.on('data', chunk => { fileChunks.push(chunk) });

      //when all chunks of a files have been read...
      readStream.on('end', async () => {

          //assemble all chunks into a file
          const file = Buffer.concat(fileChunks);
          console.log(file);

          //store file in zip folder
          await zip.file(fileName, file, { base64: true })
          console.log(index)

          downloaded++;
          zip.generateAsync({ type: "nodebuffer" })
                        .then(function (content) {

                            //deliver zip folder to font end
                            res.send(content);
                        })
                        .catch(err => {
                            next(err)
                        });
      })
    };
  })()
})

router.get('/',(req,res) => {
    (async() => {
        try {
            const collegedata = await  dbmodel.find(req.body).exec();
            return res.send({data: collegedata, status: 200, msg: "DONE"})
        } catch(err) {
            console.log("err == ", err);
            res.send({data: [], status: 500, msg: err})
        }
    })()
})

var arrUpload = upload.fields([{name:'logoimage', maxCount: 1}, {name:'collegeimage', maxCount: 1}, {name:'bannarimage', maxCount: 1}, {name:'brochurefile', maxCount: 1}, {name:'collegegallary'}]);
router.post("/post/", arrUpload, (req,res) => {
    (async() => {
        try {
            if (req.files.collegegallary){
                const filearr = [];
                for (let gallary of req.files.collegegallary){
                    filearr.push(gallary.id)
                }
                req.body.collegegallary = filearr
            }
            req.body.logoimage = req.files.logoimage ? req.files.logoimage[0].id  : null;
            req.body.collegeimage = req.files.collegeimage ? req.files.collegeimage[0].id  : null;
            req.body.bannarimage = req.files.bannarimage ? req.files.bannarimage[0].id : null;
            req.body.brochurefile = req.files.brochurefile ? req.files.brochurefile[0].id : null;
            
            const collegedata = await new dbmodel(req.body).save();
            return res.send({data: collegedata, status: 200, msg: "DONE"})
        } catch (err){ 
            console.log("err == ", err);
            res.send({data: [], status: 500, msg: err}) 
        }
    })()    
})

router.get('/delete/:pk', (req,res) => {
    dbmodel.findByIdAndRemove(req.params.pk, {useFindAndModify: false}, function(err,data){
        if(!err){ 
            res.redirect('/');
        }
    });
})

router.post('/edit/:pk', arrUpload, (req,res) => {
    if(req.files) {
        const filearr = [];
        for (var i = 0; i < req.files.length; i++){
            filearr.push(req.files[i].filename)
        }
        req.body['img'] = filearr;
    };
    dbmodel.findByIdAndUpdate(req.params.pk, req.body, {useFindAndModify: false}, function(err,data){
        if(!err){ 
            res.redirect('/');
        }
    });

})

router.get('/api/ref/', (req,res) => {
    var dict = [{ $lookup: { from: 'reference', localField: '_id', foreignField: 'user', as: 'ref_data' }}]
    dbmodel.find().populate('reference.user').exec((err, data) => {
      
        res.json(data);
      
    });
})

router.get('/ref/', (req,res) => {
    var dict = {};
    var user = dbmodel.find((err, data) => {
        dict.users = data
    })
    
    referencedbmodel.find((err, data) => {
        if(!err) {
            if (data.length != null){
                dict.data = data
                res.render('refuser', dict);
            } else {
                dict.data = ""
                res.render('refuser', dict);
            }
        }
        else {
            dict.error = err
            res.render('refuser', dict);
        }
    })  
})

router.post("/ref/post/", (req, res) => {
    try{
        console.log("vreq.body -----==--=-= ", req.body);
    var refDB = {
        user : mongoose.mongo.ObjectId(req.body.user),
        height: req.body.height,
        weight: req.body.weight,
        color: req.body.color,
        status: req.body.status,    
    }
    referencedbmodel.create(refDB, (err, item) => { 
        if (err) { 
            console.log(err); 
        } 
        else { 
            // item.save(); 
            res.redirect('/ref'); 
        } 
    });
    } catch(err) {
        res.send(err)
    }
    
})

router.post("/ref/edit/", (req, res) => {
    var regex_match = /[!@#$%^&*()_+=\[\]{};':\"\\|,.<>\/? ]/g;
    if (req.body.slug && req.body.slug.includes("-") && !regex_match.test(req.body.slug)){
        return res.json({msg: req.body.slug})
    } else {
        return res.json({msg: "slug is not in format"})
    }
})

module.exports = router;
