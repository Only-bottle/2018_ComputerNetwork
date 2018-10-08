#!/usr/bin/python3

import pygeoip
import subprocess
import cgi, cgitb

form = cgi.FieldStorage()
print ("Content-type:text/html")
print ()

print ('<html>')
print ('<head>')
print ('<meta charset="utf-8">')
print ('<title>CN_201402391</title>')
print ('</head>')

print ('<body>')
print ('<h2>Traceroute - Visualize on Kakao Map</h2>')
print ('<div id="map" style="width:500px;height:400px;"></div>')

print ("<script type='text/javascript' src='//dapi.kakao.com/v2/maps/sdk.js?appkey=176f39fad4b61f527fb42357eb5c36c7'></script>")

print ('<script>')
print ('var container = document.getElementById("map");')
print ('var options = {center : new daum.maps.LatLng(36.7844993, 126.4503169),level: 13};')
print ('var map = new daum.maps.Map(container, options);')
print ('</script>')

print ("<form method='get' action='test.cgi'>")
print ("<input type='text' name='target'/>", "<input type='submit'/>")
print ("</form>")

argv_data = form.getvalue('target') # 기존의 인자값을 form으로 받는다.

print ('<H2>Destination :  ', argv_data, '</H2>')

gi = pygeoip.GeoIP('GeoLiteCity.dat')

proc = subprocess.Popen(["traceroute", "-m", "30", argv_data], stdout = subprocess.PIPE)
out, err = proc.communicate()

output = out.decode('utf-8')
output = output.split("\n")

for i in range(1, len(output) - 1):
    outline = output[i].split()
    ip_addr = outline[1]
    if outline[1] != '*':
        if gi.record_by_addr(ip_addr) is None:
            print('(', ip_addr,')', " - No Geoloaction Info.")
            print('<br>')
        else:
            a = gi.record_by_addr(ip_addr)
            print('(', ip_addr,') -' ,' (', a.get('latitude'), a.get('longitude'), ')')
            print('<br>')
            # 지도에 마커를 표시한다.
            print ('<script>')
            print ('var markerPosition = new daum.maps.LatLng(' , a.get('latitude'),',' ,a.get('longitude'), ');')
            print ('var marker = new daum.maps.Marker({position: markerPosition});')
            print ('marker.setMap(map);')
            print ('</script>')

    elif outline[2] != '*':
        if gi.record_by_addr(ip_addr) is None:
            print('(', ip_addr,')', " - No Geoloaction Info.")
            print('<br>')
        else:
            a = gi.record_by_addr(ip_addr)
            print('(', ip_addr,') -' ,' (', a.get('latitude'), a.get('longitude'), ')')
            print('<br>')
            # 지도에 마커를 표시한다.
            print ('<script>')
            print ('var markerPosition = new daum.maps.LatLng(' , a.get('latitude'),',' ,a.get('longitude'), ');')
            print ('var marker = new daum.maps.Marker({position: markerPosition});')
            print ('marker.setMap(map);')
            print ('</script>')

print ('</body>')
print ('</html>')

