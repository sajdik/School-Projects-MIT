#!/bin/sh

#aggregate table for better manipulation
echo $(mongo upa --eval 'db.days.aggregate([
 	{$unwind: "$currencies"},
 	{$project: { _id:0,field_id:"$_id",currency: "$currencies", "date": 1}},
 	{$out: "aggregate_upa"} 
 	]).toArray()')

#export and copy table in json 
echo $(mongoexport --db upa --collection aggregate_upa --noHeaderLine --fields date,currency --out /shared/info.json)
