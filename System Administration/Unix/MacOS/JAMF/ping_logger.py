import pythonping as pyping
from datetime import datetime
import os

today = datetime.now()
user = os.path.expanduser('~')
filepath = f'{user}/Desktop/ping-test-{today}.csv'


def clear():
	os.system('clear')

def ping_test():
	target = "8.8.8.8"
	count = int(input(f"How many pings do you want to send?\n"))
	size = 56
	interval = 1
	clear()
	print(f"""
Starting ping test, sending {count} pings to {target}.
Destination file: {filepath}

Test started at {today}""")
	with open(filepath, 'w') as f:
		print(pyping.ping(target, count = count, size = size, interval = interval), file=f)
	f.close()
	print(f"Test ended at {datetime.now()}\n\nPing test complete.")
		
		
if __name__ == "__main__":
	clear()
	ping_test()