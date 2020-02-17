import subprocess as sub
import os
import mutagen
import mutagen.mp3
from mutagen.easyid3 import EasyID3
import datetime
import time
import signal
import glob

# Edit mp3 tag
def edit_mp3_tag(transfer_file):
    try:
        meta = EasyID3(transfer_file)
    except mutagen.id3.ID3NoHeaderError:
        meta = mutagen.File(transfer_file, easy=True)
        meta.add_tags()
        
        date = datetime.date.today()
        meta['title'] = str(date) + "_leebyeongman"
        meta['artist'] = "201402391"
        meta.save()

def kbs_download():
    now = datetime.datetime.now()
    date = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
    
    # variables
    original_file = './original_path/' + date + '_KBS' + '.flv'
    transfer_file = './transfer_path/' + date + '_KBS' + '.mp3'
    cmd = 'mplayer -ao pcm:file=' + original_file + ' $(curl -s "http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=24&ch_type=radioList" | grep service_url | tail -1 | cut -d\\\" -f16 | cut -d\\\\ -f1) -vc dummy -vo null'

    # KBS radio download 
    proc = sub.Popen(cmd, shell=True, preexec_fn=os.setsid)
    time.sleep(30)
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    # transfer flv to mp3
    proc = sub.Popen(["ffmpeg", "-i", original_file, "-acodec", "mp3", transfer_file], stdout = sub.PIPE)
    proc.communicate()

    # Edit_excute
    edit_mp3_tag(transfer_file)

def ebs_download():
    now = datetime.datetime.now()
    date = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
    ip = "rtmp://58.229.187.11/iradio/iradiolive_m4a"
    original_file = './original_path/' + date + '_EBS' + '.flv'
    transfer_file = './transfer_path/' + date + '_EBS' + '.mp3'

    # EBS radio download
    proc = sub.Popen(["rtmpdump", "-r", ip, "-B", "10", "-o", original_file], stdout=sub.PIPE)
    proc.communicate()

    # Transfer flv to mp3
    proc = sub.Popen(["ffmpeg", "-i", original_file, "-acodec", "mp3", transfer_file], stdout=sub.PIPE)
    proc.communicate()

    # Edit_excute
    edit_mp3_tag(transfer_file)

def create_html():
    f = open('download.html', 'w')
    
    f.write('<html>\n')
    f.write('   <head>\n')                                                                        
    f.write('       <meta charset="utf-8">\n')                                                    
    f.write('       <title>Download</title>\n')                                                   
    f.write('   </head>\n')                                                                       

    f.write('   <body>\n')
    kbs_file = glob.glob('/home/leebyeongman/CN_201402391/10/transfer_path/*_KBS.mp3')            
    ebs_file = glob.glob('/home/leebyeongman/CN_201402391/10/transfer_path/*_EBS.mp3')            
    print(kbs_file)                                                           
    print(ebs_file)                                                                               
    f.write('   <h2>KBS_RADIO_List</h2>\n')
    j = 1
    for i in kbs_file:
        f.write('       <a href="'+'./'+i.split('/')[5]+'/'+i.split('/')[6]+'" download>'+ str(j) +'.</a>\n')
        j += 1

    f.write('   <h2>EBS_RADIO_List</h2>\n')
    j = 1
    for i in ebs_file:
        f.write('       <a href="'+'./'+i.split('/')[5]+'/'+i.split('/')[6]+'" download>'+ str(j) +'.</a>\n')
        j += 1

    f.write('   </body>\n')
    f.write('</html>\n')

kbs_download()
ebs_download()
create_html()
