select * from colleges inner join refdbs on colleges._id = refdbs.college inner join collegeinfos on colleges._id = collegeinfos.college;
