#!/usr/bin/python
# Reads /var/run/miner.output and averages out various stats per GPU
# You should zero out the log file between config changes
#
# 1) modify your config with new overclock settings
# 2) putconf
# 3) minestop ; ethos-overclock ; >/var/run/miner.output ; minestart

i = 0
soltotal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
wtotal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
intervalreset = 0


f = open('/var/run/ethos/gpucount.file',"r")
line = f.readline()
f.close()

line = line.strip()

gpucount = int(line)
print "GPUCOUNT: %d " % (gpucount)


f = open('/var/run/miner.output',"r")
lines = f.readlines()
f.close()

for line in lines:
	if line.startswith('|  '):
		gpuid = line[3]
		gpuid = int(gpuid)
		#print "GPUID: %s" % (gpuid)
		if intervalreset == 0:
			i += 1
			intervalreset = 1
		splitted = line.split()
		w = splitted[3]
		w = w[:-1]
		wtotal[gpuid] += float(w)
		sol = splitted[5]
		soltotal[gpuid] += float(sol)
	else:
		intervalreset = 0

print "%d samples read from /var/run/miner.output" % (i)
for z in range(0,gpucount):
	print "GPU %d: %.2f Sol/W.  Watt average = %.2f.  Sol average = %.1f" %  (z,soltotal[z]/i,wtotal[z]/i,((soltotal[z]/i)*(wtotal[z]/i)))
