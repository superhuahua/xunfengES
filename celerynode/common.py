import hashlib
import re
import urllib2

def get_ip_list(ip):
    #hosts = "10.151.136.0/24" CIDR
    #hosts = "10.151.136.0-10.151.136.10"
    ip_list_tmp = []
    iptonum = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    numtoip = lambda x: '.'.join([str(x / (256 ** i) % 256) for i in range(3, -1, -1)])
    if '-' in ip:
        ip_range = ip.split('-')
        ip_start = long(iptonum(ip_range[0]))
        ip_end = long(iptonum(ip_range[1]))
        ip_count = ip_end - ip_start
        if ip_count >= 0 and ip_count <= 655360:
            for ip_num in range(ip_start, ip_end + 1):
                ip_list_tmp.append(numtoip(ip_num))
        else:
            print '-h wrong format'
    else:
        ip_split = ip.split('.')
        net = len(ip_split)
        if net == 2:
            for b in range(1, 255):
                for c in range(1, 255):
                    ip = "%s.%s.%d.%d" % (ip_split[0], ip_split[1], b, c)
                    ip_list_tmp.append(ip)
        elif net == 3:
            for c in range(1, 255):
                ip = "%s.%s.%s.%d" % (ip_split[0], ip_split[1], ip_split[2], c)
                ip_list_tmp.append(ip)
        elif net == 4:
            ip_list_tmp.append(ip)
        else:
            print "-h wrong format"
    return ip_list_tmp

def get_id_md5(host, port):
    h = hashlib.md5()
    h.update("{0}:{1}".format(host, port))
    return h.hexdigest()

def get_code(header, html):
    try:
        m = re.search(r'<meta.*?charset=(.*?)"(>| |/)', html, flags=re.I)
        if m: return m.group(1).replace('"', '')
    except:
        pass
    try:
        if 'Content-Type' in header:
            Content_Type = header['Content-Type']
            m = re.search(r'.*?charset=(.*?)(;|$)', Content_Type, flags=re.I)
            if m: return m.group(1)
    except:
        pass

#@param
#   task_netloc list: [host, port]
#   pluginInfo list: {"url":"", "method":"", "data":""}

def set_request(task_netloc, pluginInfo):
    url = 'http://' + task_netloc[0] + ":" + str(task_netloc[1]) + pluginInfo['url']
    if pluginInfo['method'] == 'GET':
        request = urllib2.Request(url)
    else:
        request = urllib2.Request(url, pluginInfo['data'])
    return request