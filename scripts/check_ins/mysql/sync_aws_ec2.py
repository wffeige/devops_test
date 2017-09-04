#!/usr/bin/env python


import os, sys, subprocess, json, datetime, time, re
from MyLink import MySQL
from MT import *

my_config = get_rds_info_dict('rep')

def sync_ec2():
    date_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    sync_cmd = "/usr/bin/aws ec2 describe-instances"
    ec2_str = shell(sync_cmd, 'r')
    ec2_json = json.loads(ec2_str)
    ec2_res_lst = []
    privateip_lst = []
    ec2_one_dict = {}
    mysql = MySQL(my_config)
    local_sql = "select privateip from ec2_instance_pool"
    local_res = mysql.result_lst(local_sql)
    local_res_lst = [line[0] for line in local_res]
    for one in ec2_json['Reservations']:
        instance_lst = one['Instances']
        for instance in instance_lst:
            tag = 'NULL'
            try:
                for i in instance['Tags']:
                    if i['Key'] == 'Name':
                        name = i['Value']
                    elif i['Key'] == 'Type':
                        tag = i['Value']
                    if tag == 'online_db':
                        group_id = name.split('_')[-1]
                    else:
                        group_id = 'NULL'
            except:
                name, tag = 'NULL', 'NULL'
            try:
                instance_id = instance['InstanceId']
            except:
                instance_id = 'NULL'
            try:
                volumeid = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']
            except:
                volumeid = 'NULL'
            try:
                state = instance['State']['Name']
            except:
                state = 'NULL'
            try:
                securitygroups = instance['SecurityGroups'][0]['GroupName']
            except:
                securitygroups = 'NULL'
            try:
                instancetype = instance['InstanceType']
            except:
                instancetype = 'NULL'
            try:
                availabilityzone = instance['Placement']['AvailabilityZone']
            except:
                availabilityzone = 'NULL'
            try:
                launchtime = instance['LaunchTime']
            except:
                launchtime = 'NULL'
            for i in ('-', 'T', 'Z', ':', '.'):
                launchtime = launchtime.replace(i, ' ')
            launchtime_lst = [ i for i in launchtime.split() ]
            d1 = datetime.datetime(int(launchtime_lst[0]), int(launchtime_lst[1]), int(launchtime_lst[2]), int(launchtime_lst[3]), int(launchtime_lst[4]), int(launchtime_lst[5]))
            d2 = d1 + datetime.timedelta(hours=8)
            network = instance['NetworkInterfaces']
            try:
                publicip = network[0]['Association']['PublicIp']
            except:
                publicip = 'NULL'
            try:
                pyblicdnsname = network[0]['Association']['PublicDnsName']
            except:
                pyblicdnsname = 'NULL'
            try:
                privateip = network[0]['PrivateIpAddresses'][0]['PrivateIpAddress']
            except:
                privateip = 'NULL'
            try:
                privatednsname = network[0]['PrivateDnsName']
            except:
                privatednsname = 'NULL'
            if len(network) > 1:
                try:
                    privateip2 = network[1]['PrivateIpAddresses'][0]['PrivateIpAddress']
                    privatednsname2 = network[1]['PrivateIpAddresses'][0]['PrivateDnsName']
                except:
                    privateip2, privatednsname2 = 'NULL', 'NULL'
            else:
                privateip2, privatednsname2 = 'NULL', 'NULL'
            try:
                vpcid = network[0]['VpcId']
            except:
                vpcid = 'NULL'
            if vpcid == 'vpc-454e4120':
                environment = 'beta'
            elif vpcid == 'vpc-93c785f6':
                environment = 'online'
            elif vpcid == 'vpc-edeae788':
                environment = 'dev'
            elif vpcid == 'vpc-0d1c0768':
                environment = 'network'
        ###
            if privateip in local_res_lst:
                sql = "update ec2_instance_pool set ins_name='%s',ins_tag='%s', ins_id='%s', volumeid='%s', state='%s', environment='%s', instancetype='%s', availabilityzone='%s', launchtime='%s', securitygroups='%s', privateip='%s', privatednsname='%s', publicip='%s', pyblicdnsname='%s', privateip2='%s', privatednsname2='%s', update_time='%s', group_id='%s' where privateip='%s'" % (name, tag, instance_id, volumeid, state, environment, instancetype, availabilityzone, d2, securitygroups, privateip, privatednsname, publicip, pyblicdnsname, privateip2, privatednsname2, date_time, group_id, privateip)
            elif privateip not in local_res_lst:
                sql = "insert into ec2_instance_pool (ins_name,ins_tag,ins_id,volumeid,state,environment,instancetype,availabilityzone,launchtime,securitygroups,privateip,privatednsname,publicip,pyblicdnsname,privateip2,privatednsname2,update_time,group_id) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (name, tag, instance_id, volumeid, state, environment, instancetype, availabilityzone, d2, securitygroups, privateip, privatednsname, publicip, pyblicdnsname, privateip2, privatednsname2, date_time, group_id)
            mysql.commit(sql)
            ###delete
            privateip_lst.append(str(privateip))
    for i in local_res_lst:
        if i not in privateip_lst and re.match('10', i):
            del_sql = "delete from ec2_instance_pool where privateip='%s'" % i
            mysql.commit(del_sql)
    return

def sync_disk():
    sync_cmd = "/usr/bin/aws ec2 describe-volumes"
    disk_str = shell(sync_cmd, 'r')
    disk_json = json.loads(disk_str)
    disk_res_lst = []
    mysql = MySQL(my_config)
    for one in disk_json['Volumes']:
        try:
            state = one['State']
        except:
            state = 'NULL'
        if state == 'in-use':
            try:
                size = one['Size']
            except:
                size = 'NULL'
            try:
                volumeid = one['VolumeId']
            except:
                volumeid = 'NULL'
            try:
                volumetype = one['VolumeType']
            except:
                volumetype = 'NULL'
            if volumetype == 'gp2':
                disk_type = 'SSD'
            elif volumetype == 'standard':
                disk_type = 'SAS'
            elif volumetype == 'io1':
                disk_type = 'PIOPS'
            sql = "update ec2_instance_pool set disk_size=%s, disk_type='%s' where volumeid='%s'" % (size, disk_type, volumeid)
            mysql.commit(sql)
        else:
            pass
    return

def main():
    sync_ec2()
    sync_disk()

if __name__ == "__main__":
    main()
