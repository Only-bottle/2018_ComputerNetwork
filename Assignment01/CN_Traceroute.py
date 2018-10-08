import pygeoip
import sys
import subprocess

gi = pygeoip.GeoIP('GeoLiteCity.dat')

print("[Destination]  ", sys.argv[1])
proc = subprocess.Popen(["traceroute", "-m", "30", sys.argv[1]], stdout = subprocess.PIPE)
out, err = proc.communicate()

output = out.decode('utf-8')
output = output.split("\n")

for i in range(1, len(output) - 1):
    outline = output[i].split()
    ip_addr = outline[1]
    if outline[1] != '*':
        if gi.record_by_addr(ip_addr) is None:
            print('[IP] ', ip_addr, " - No Geoloaction Info.")
        else:
            a = gi.record_by_addr(ip_addr)
            print('[IP] ', ip_addr, ',  Lat : ', a.get('latitude'), ',  Lon : ', a.get('longitude'))

    elif outline[2] != '*':
        if gi.record_by_addr(ip_addr) is None:
            print('[IP] ', ip_addr, " - No Geoloaction Info.")
        else:
            a = gi.record_by_addr(ip_addr)
            print('[IP] ', ip_addr, ',  Lat : ', a.get('latitude'), ',  Lon : ', a.get('longitude'))

