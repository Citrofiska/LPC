import requests
import time
import csv
from pythonosc import udp_client

if __name__ == "__main__":

	# Smart-me API
	url = "https://api.smart-me.com/api/Devices/"
	username = "" # your username at smart-me
	password = "" # your password at smart-me

	# OSC protocol
	ip_local_osc = "" # your IP address of the local device(laptop)
	port_osc = 5011 # osc port where the data will be sent
	client = udp_client.SimpleUDPClient(ip_local_osc, port_osc)

	print('Sending data through OSC protocol')
	print('-'*30)
	Voltage_list = []
	Current_list = []
	ActivePower_list = []
	Energy_list = []
	old_time = time.time()
	diff = 1
	old_energy = 0
	thres = 10e-5
	iter = 0

	while diff>thres:

		response = requests.get(url, auth=(username, password))
		devices = response.json()
		ActivePower = devices[0]['ActivePower'] * 1000
		Voltage = devices[0]['Voltage']
		Current = devices[0]['Current']
		PowerFactor = devices[0]['PowerFactor']
		Temperature = devices[0]['Temperature']

		time_interval = time.time() - old_time
		old_time = time.time()
		energy = ( ActivePower / 1000 ) * ( time_interval / 3600 )
		client.send_message("/smart-me/Voltage", Voltage)
		client.send_message("/smart-me/Current", Current)
		client.send_message("/smart-me/Power", ActivePower)
		client.send_message("/smart-me/Energy", energy) # energy in kWh

		print(f"receiving new data from smart-me at {old_time}")

		# print("/smart-me/Voltage", Voltage)
		# print("/smart-me/Current", Current)
		# print("/smart-me/Power", ActivePower)
		# print("/smart-me/Energy", energy)
		print(f"saving new data from smart-me at {old_time}")

		Voltage_list.append(Voltage)
		Current_list.append(Current)
		ActivePower_list.append(ActivePower)
		Energy_list.append(energy)

		diff = energy - old_energy
		old_energy = energy
		iter += 1
		print(f"Energy diff is {diff} at {iter} counting")

		time.sleep(30)

	# write energy list to csv
	with open('output_energy.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		for item in Energy_list:
			writer.writerow([item])

# Xu edit on 6/21