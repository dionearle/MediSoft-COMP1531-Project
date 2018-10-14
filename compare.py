from datetime import datetime, timedelta

if __name__ == '__main__':

	listDates = [datetime.strptime("24/09/1999", "%d/%m/%Y"), datetime.strptime("01/09/1999", "%d/%m/%Y"),
				datetime.strptime("31/12/1999", "%d/%m/%Y")]

	listDates.sort()

	print(str(listDates))