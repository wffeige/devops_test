#!/usr/bin/python
import difflib
import sys

try:



    textfile1='web_info_timestamp.txt'
    # textfile2='/root/devops/scripts/controller/guanlian/var/log_time_controller.txt'
    textfile2='/root/devops/scripts/controller/guanlian/var/log_time_compute.txt'



except Exception,e:
    print "Error:"+str(e)
    print "Usage: simple3.py filename1 filename2"
    sys.exit()

def readfile(filename):
    try:
        fileHandle = open (filename, 'rb' )
        text=fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
       print('Read file Error:'+str(error))
       sys.exit()

def main():
    text1_lines = readfile(textfile1)
    text2_lines = readfile(textfile2)

    d = difflib.HtmlDiff()
    # print d.make_file(text1_lines, text2_lines)
    with open ('./diff.html','w') as e:
        e.write(d.make_file(text1_lines, text2_lines))
        e.close()

if __name__ == "__main__":
    main()


