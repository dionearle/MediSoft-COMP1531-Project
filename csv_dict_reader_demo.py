import csv

# files from:
# https://support.spatialkey.com/spatialkey-sample-csv-data/

# relevant Python3 documentation:
# https://docs.python.org/3/library/csv.html#csv.DictReader

# this is just the first row in a list...
COLUMNS = [
	'street',
	'city',
	'zip',
	'state',
	'beds',
	'baths',
	'sq__ft',
	'type',
	'sale_date',
	'price',
	'latitude',
	'longitude'
]

# program to print all transactions with date and prices
if __name__ == '__main__':
	with open('Sacramentorealestatetransactions.csv') as f:
		reader = csv.DictReader(f)
		for row in reader:
			print('we sold a property at {} for ${} on {}'.format(row['street'], row['price'], row['sale_date']))