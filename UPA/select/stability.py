#!/usr/bin/python

import psycopg2
import sys
import datetime

host = "postgresql-service"
database = "upa"
user = "upa"
password = "upa"


def parse_arguments(args):
    #the least changing currency is the most stable 
    if len(args) == 3 or ( len(args) == 4 and args[3].upper() == "DESC"):
        order_type = "ASC"
    elif len(args) == 4 and args[3].upper() == "ASC":
        order_type = "DESC"
    else:
        raise ValueError("Invalid arguments")

    return parse_date(args[1], args[2]), order_type


def parse_date(from_date, to_date):
    return str(datetime.datetime.strptime(from_date, "%d.%m.%Y").date()), str(datetime.datetime.strptime(to_date, "%d.%m.%Y").date())


def get_results((from_date, to_date), order_type):
    connection = psycopg2.connect(host = host , database = database, user = user, password = password)
    cursor = connection.cursor()
    #  sum(abs((actual/average)-1)) in period
    cursor.execute("select name, \
        sum(abs((rate / (select avg(c.rate) as average from currencies c where c.name=cur.name and c.date BETWEEN '" + from_date + "' and '" + to_date +"' group by c.name))-1)) as stability \
        from currencies cur where cur.date BETWEEN '" + from_date + "' and '" + to_date +"'\
        group by name order by stability \
        " + order_type)
    data = cursor.fetchall()
    connection.close()
    return data


def print_results(results, (from_date, to_date)):
    print("Currency stability from " + from_date + " to " + to_date + " ranking")
    print("RANK | CURRENCY | ABSOLUTE DEVIATION IN %")
    print("_________________________________________")
    for i in range(len(results)):
        if results[i][1] == None:
            print("{:02d}.  | {}      | missing data".format(i+1, results[i][0]))
        else:
            print("{:02d}.  | {}      | {:.3f} %".format(i+1, results[i][0], float(results[i][1])*100))


def print_usage():
    print("Usage: ./stability.py <from date> <to_date> [ASC/DESC]")
    print("date is in format DD.MM.YYYY")


try:
    period, order_type = parse_arguments(sys.argv)
    results = get_results(period, order_type)
    print_results(results, period)

except ValueError:
    print_usage()
    exit(1)  
