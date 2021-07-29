#!/usr/bin/python

import psycopg2
import sys
import datetime

host = "postgresql-service"
database = "upa"
user = "upa"
password = "upa"


def parse_arguments(args):
    if len(args) == 3 or ( len(args) == 4 and args[3].upper() == "DESC"):
        order_type = "DESC"
    elif len(args) == 4 and args[3].upper() == "ASC":
        order_type = "ASC"
    else:
        raise ValueError("Invalid arguments")

    return parse_date(args[1], args[2]), order_type


def parse_date(from_date, to_date):
    return str(datetime.datetime.strptime(from_date, "%d.%m.%Y").date()), str(datetime.datetime.strptime(to_date, "%d.%m.%Y").date())


def get_results((from_date, to_date), order_type):
    connection = psycopg2.connect(host = host , database = database, user = user, password = password)
    cursor = connection.cursor()

    cursor.execute("select distinct cur.name, \
                ((select rate from currencies c where c.date='" + to_date + "' and c.name=cur.name limit 1) \
                /(select rate from currencies c where c.date='" + from_date + "' and c.name=cur.name limit 1))-1 \
                as change from currencies cur order by change " + order_type )
    data = cursor.fetchall()
    connection.close()
    return data


def print_results(results, from_date, to_date):
    print("Currency strengthening from " + from_date + " to " + to_date + " leaderboard")
    print("RANK | CURRENCY | STRENGTH CHANGE IN %")
    print("______________________________________")
    for i in range(len(results)):
        if results[i][1] == None:
            print("{:02d}.  | {}      | missing data".format(i+1, results[i][0]))
        else:
            print("{:02d}.  | {}      | {:+.3f} %".format(i+1, results[i][0], float(results[i][1])*100))


def print_usage():
    print("Usage: ./strength.py <from date> <to_date> [ASC/DESC]")
    print("date is in format DD.MM.YYYY")


try:
    period, order_type = parse_arguments(sys.argv)
    results = get_results(period, order_type)
    print_results(results, sys.argv[1], sys.argv[2])

except ValueError:
    print_usage()
    exit(1)  
