import csv

from hobbibi.models import Hobbi

csv_path = '/home/luca/cs50w/finalproject/final/hobbies.csv'

with open(csv_path) as f:
    reader = csv.reader(f)
    for row in reader:
        hobbi = Hobbi.objects.create(name= str(row[0]))
        hobbi.save()

