#!/bin/sh

file='/shared/info.json'
query='
CREATE TABLE IF NOT EXISTS "currencies" (
"date" DATE NULL,
"name" TEXT NULL,
"rate" FLOAT NULL
);'

#create table and set datestyle
PGPASSWORD=upa psql -h localhost -U upa -d upa -c "$query"

query='INSERT INTO currencies (date, name, rate) VALUES '
num=0

#loop trough all revelant results
for k in $(jq -r ' .date, .currency.name, .currency.rate' $file)
do
	let num++
	#save date value
	if [ $(expr $num % 3) -eq 1 ]; then
		split=(${k//./ })
		date=${split[2]}'-'${split[1]}'-'${split[0]}
	#save name value
	elif [ $(expr $num % 3)  -eq 2 ]; then
		name=$k
	else
		query+='('\'''$date''\''',''\'''$name''\''',$k'),'
		#every 1000 items insert into table in psql db
		if [ $num -gt 3000 ]; then
			mod=${query//[\"]/\'}
			mod=$(echo "${mod}" | sed 's/.$//');
			#send insert query
			PGPASSWORD=upa psql -h localhost -U upa -d upa -c "$mod"
			num=0
			query='INSERT INTO currencies (date, name, rate) VALUES '
		fi
	fi
done

mod=${query//[\"]/\'}
mod=$(echo "${mod}" | sed 's/.$//');
#insert remaining items
PGPASSWORD=upa psql -h localhost -U upa -d upa -c "$mod"
