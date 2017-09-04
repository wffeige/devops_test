#!/usr/bin/env python

import os, sys, getopt, logging, subprocess, json

def logger(logfile):
    logpath_lst = logfile.split('/')
    logpath_lst = logpath_lst[:-1]
    logpath = '/'.join(logpath_lst)
    if not os.path.isdir(logpath):
        os.makedirs(logpath)
    format = '%(asctime)s [%(filename)s][%(levelname)s] %(message)s'
    logging.basicConfig(level = logging.DEBUG, filename = logfile, filemode = 'a', format = format)
    logger = logging.getLogger()
    return logger

def deco_head(logfile):
    def deco_opt(func):
        def opt(*args, **kwargs):
            try:
                opts, args = getopt.getopt(sys.argv[1:], "o", ["opt=", "discovery="])
            except getopt.GetoptError, err:
                print 0.0
                sys.exit(1)
            opt_dict = {}
            for k, v in opts:
                if k in ("--opt"):
                    opt_dict['opt'] = v
                if k in ("--discovery"):
                    discovery_value = v
                else:
                    discovery_value = ''
            if 'opt' not in opt_dict.keys():
                print 0.0
                sys.exit(1)
            else:
                opt_value = opt_dict['opt']
            ###
            logging = logger(logfile)
            return func(opt_value, discovery_value, logging)
        return opt
    return deco_opt

def shell(cmd, type = 's'):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        if type == 's':
            return p_status
        elif type == 'r':
            return output.strip()
    except Exception, e:
        return 

class TmpFile:
    
    def __init__(self, tmpfile):
        self.tmpfile = tmpfile
    
    def recode_info(self, info):
        """
        """
        in_put = open(self.tmpfile, 'w')
        in_put.writelines(info)
        in_put.close()

    def get_content(self):
        """
        """
        try:
            out_put = open(self.tmpfile)
            content = out_put.readline()
            out_put.close()
        except:
            return {}
        return dict(eval(content))


