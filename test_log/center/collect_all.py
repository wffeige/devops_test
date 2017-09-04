# encoding:utf-8
#!/usr/bin/python

import sys
import subprocess
import threading
import ansible.runner
from time import ctime,sleep

#集群机器列表
machine_lst=['172.16.1.134','172.16.1.135','172.16.1.136','172.16.1.138']

try:
    clas = sys.argv[1]
    date = sys.argv[2]
    time_start = sys.argv[3]
    time_stop = sys.argv[4]
except IndexError as e:
    print "参数错误！\nUsage: python script.py [method]  [date] [start_time]  [stop_time] \nExample: python script.py error '2017-08-22' '00:00:00'  '00:01:00'"
    sys.exit()

def shell(cmd, type='s'):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        if type == 's':
            return p_status
        elif type == 'r':
            print  p.stdout.readline()
            return p.stdout.readline()

            # return output.strip()
    except Exception, e:
        return 0

def command(pattern, module, args, fork):
    results = ansible.runner.Runner(pattern=pattern, forks=fork,module_name=module, module_args=args,).run()

    for (hostname, result) in results['contacted'].items():
        try:
            if not 'failed' in result:
                print "{} collect sucessful!".format(hostname)
        except Exception, e:
            print e
            sys.exit(1)


def allnode_together(clas,src_txt):
    for host in machine_lst:
        cmd = "scp {host}:{src_txt} /root/devops/scripts/center/var/all/{name}_{method}.txt".format(host=host,src_txt=src_txt,method=clas,name=host.split(".")[-1])
        shell(cmd)
    cmd = "cat /root/devops/scripts/center/var/all/*_{method}.txt |sort -n -k2 >/root/devops/scripts/center/var/all/res_{method}.txt".format(method=clas,)

    shell(cmd)

def execute(clas):
    if clas == "error":
        scripts="/root/devops/scripts/log_analyze/error_log.py"
        src_txt = "/root/devops/scripts/log_analyze/var/result_con_err.txt"
    elif clas == "relation":
        scripts = "/root/devops/scripts/log_analyze/relation_log.py"
        src_txt = "/root/devops/scripts/log_analyze/var/result_con_rel.txt"
    else:
        print "class is not true"
        return 1

    threads = []

    t1 = threading.Thread(target=command, args=('172.16.1.134', 'command', 'python {scripts} {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,scripts=scripts), 1))
    threads.append(t1)

    t2 = threading.Thread(target=command, args=('172.16.1.135', 'command', 'python {scripts} {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,scripts=scripts), 1))
    threads.append(t2)

    t4 = threading.Thread(target=command, args=('172.16.1.136', 'command', 'python {scripts} {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,scripts=scripts), 1))
    threads.append(t4)

    t3 = threading.Thread(target=command, args=('172.16.1.138', 'command', 'python {scripts}  {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,scripts=scripts), 1))
    threads.append(t3)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    allnode_together(clas,src_txt)
    print "All collecting sucessful!"





def main():
    execute(clas)


if __name__ == "__main__":
    main()


