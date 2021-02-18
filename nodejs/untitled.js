db.getCollection("colleges").aggregate([
        { 
            "$project" : { 
                "_id" : NumberInt(0), 
                "colleges" : "$$ROOT"
            }
        }, 
        { 
            "$lookup" : { 
                "localField" : "colleges._id", 
                "from" : "refdbs", 
                "foreignField" : "college", 
                "as" : "refdbs"
            }
        }, 
        { 
            "$unwind" : { 
                "path" : "$refdbs", 
                "preserveNullAndEmptyArrays" : false
            }
        }, 
        { 
            "$lookup" : { 
                "localField" : "colleges._id", 
                "from" : "collegeinfos", 
                "foreignField" : "college", 
                "as" : "collegeinfos"
            }
        }, 
        { 
            "$unwind" : { 
                "path" : "$collegeinfos", 
                "preserveNullAndEmptyArrays" : false
            }
        }
    ], 
    { 
        "allowDiskUse" : true
    })
