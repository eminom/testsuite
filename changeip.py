

import socket
import re, sys

pat = re.compile(r"^(\d+)\.(\d+).(\d+)\.(\d+)$")

def go(ip):
	addr = (ip, 11100)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.bind(addr)
	#s.listen(5)
	print("connecting to %s" % (ip))
	s.connect(addr)
	s.send('http://192.168.18.1:12000/version.php' + "\r\n")
	data = s.recv(512)
	print("recv<" + str(data) + ">")
	return
	
if '__main__' == __name__:
	if len(sys.argv) != 2:
		print("Need more parameter")
		sys.exit(-1)
	if not pat.match(sys.argv[1]):
		print("Need a target ip")
		sys.exit(-1)
	go(sys.argv[1])
	#go()

