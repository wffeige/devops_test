#!/usr/bin/env python
# -*- coding:utf8 -*-
'''
discovery
    --opt=discovery

get the Read KB/s of interface
    --opt=rkps --descovery=$1

get the Write KB/s of interface
    --opt=tkps --descovery=$1

get the Total error rate of interface
    --opt=errrate --descovery=$1

'''
import os, sys, tempfile
from common_zabbix import deco_head, logger, shell, TmpFile

base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])

def discovery_info():
    '''
    discovery the active network interface, output with json format
    '''
    print "{";
    print '''\t"data":['''
    cmd = r'''ip -o addr show up|grep "inet "|awk -F ":" '{print $2}'|awk '{print $1}' '''
    cmdout = shell(cmd, 'r')
    linenum = 0
    lineslist = cmdout.strip().split('\n')
    if 'lo' in lineslist:
        lineslist.remove('lo')
    aset = set()
    for line in lineslist:
        if line.strip() == '': continue
        aset.add(line.strip())
    listlen = len(aset)    
    for line in aset:
        linenum += 1
        if linenum != listlen:
            print '''\t\t{"{#IFNAME}": "%s"},''' % line
        else:
            print '''\t\t{"{#IFNAME}": "%s"}''' % line
    print '''\t]\n}'''

def network_dict(ifname):
    '''
    use command 'sar -n DEV 1 2', use the average line, unit KB
    '''
    cmd = r'sar -n DEV 1 2'
    network_str = shell(cmd, 'r')
    network_lst = []
    for line in network_str.split('\n'):
        if line == '':
            network_lst = []
        else:
            network_lst.append(line)
    try:
        title_lst = network_lst[0].split()[1:]
        values_lst = [i.split() for i in network_lst if ifname in i.split()][0][1:]
        network_dict = dict(zip(title_lst, values_lst))
    except:
        return {}
    return network_dict

def net_error(ifname):
    '''
    use command 'ifconfig eth0', (Read errors + Write errors) / (Read total + Write total)
    '''
    cmd = "ifconfig %s | grep errors" % ifname
    errs = 0
    total = 0
    error_info_str = shell(cmd, 'r')
    for line in error_info_str.split('\n'):
        if line.strip() == '': continue
        try:
            line2 = line.strip().replace(":", " ")
            alist = line2.split()
            errs += int(alist[4])
            total += int(alist[2])
        except Exception, e:
            return
    if total == 0:
        return 0.0
    else:
        print "_____this_____"
        return "%.2f" % (100.0 * (float(errs) / float(total)))

@deco_head(logfile)
def main(opt, discovery, logging):
    if opt == 'discovery':
        discovery_info()
    elif opt == 'errrate':
        net_error_info = net_error(discovery)
        if net_error_info:
            print net_error_info
        else:
            logging.error("Network get error, check 'ifconfig' pls.")
    else:
        cache_file = r'%s/var/%s_%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0], discovery)
        cache = TmpFile(cache_file)
        if opt == 'rkps':
            # network_info_dict = network_dict(discovery)
            network_info_dict = network_dict(discovery)
            if isinstance(network_info_dict, dict):
                print float(network_info_dict.setdefault('rxkB/s', 0))
            else:
                logging.error("Network get error, check 'sar -n DEV 1 2' pls.")
                network_info_dict = ''
                print 0.0
            ###cache
            cache.recode_info(str(network_info_dict.items()))
        else:
            network_info_dict = cache.get_content()
            if opt == 'tkps':
                print float(network_info_dict.setdefault('txkB/s', 0))
            else:
                print 0.0

if __name__ == '__main__':
    main()
