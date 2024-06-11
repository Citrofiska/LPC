import requests
import time
from pythonosc import udp_client

if __name__ == "__main__":

	# Smart-me API
	url = "https://api.smart-me.com/api/Devices/"
	username = "xuwa@kth.se" # your username at smart-me
	password = "KTHpsw4XW" # your password at smart-me

	# OSC protocol
	ip_local_osc = "130.229.191.63" # your IP address of the local device  # 172.20.10.11  130.229.191.63
	port_osc = 5011 # osc port where the data will be sent
	client = udp_client.SimpleUDPClient(ip_local_osc, port_osc)
	old_time = time.time()

	print('Sending data through OSC protocol')
	print('-'*30)
	Voltage_list = []
	Current_list = []
	ActivePower_list = []
	Energy_list = []

	while True:

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

		print("/smart-me/Voltage", Voltage)
		print("/smart-me/Current", Current)
		print("/smart-me/Power", ActivePower)
		print("/smart-me/Energy", energy)

		# save data in lists
		Voltage_list.append(Voltage)
		Current_list.append(Current)
		ActivePower_list.append(ActivePower)
		Energy_list.append(energy)

		time.sleep(1)
