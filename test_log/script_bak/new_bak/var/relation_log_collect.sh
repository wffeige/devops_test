> /root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/keystone/keystone-tokenflush.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/keystone/keystone.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/ceph/ceph.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/ceph/ceph.audit.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/ceph/ceph-mon.ztx-controller-135.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/glance/api.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/glance/registry.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/cinder-manage.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/api.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/scheduler.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/volume.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-novncproxy.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-cert.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-consoleauth.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-api.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-scheduler.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-conductor.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="2017-08-25" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/neutron/server.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="Aug" && $2=="25" &&$3>="10:00:00" && $3<="10:01:00") print $0}' /var/log/messages >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="Aug" && $2=="25" &&$3>="10:00:00" && $3<="10:01:00") print $0}' /var/log/keepalived.log >>/root/devops/scripts/new/var/result_con_rel.txt
awk -F " " '{if ($1=="Aug" && $2=="25" &&$3>="10:00:00" && $3<="10:01:00") print $0}' /var/log/haproxy.log >>/root/devops/scripts/new/var/result_con_rel.txt
cat /var/log/httpd/access_log| egrep '25/Aug/2017:10:00' >>/root/devops/scripts/new/var/result_con_rel.txt
cat /var/log/httpd/access_log| egrep '25/Aug/2017:10:01' >>/root/devops/scripts/new/var/result_con_rel.txt
cat /var/log/httpd/error_log| egrep '25/Aug/2017:10:00' >>/root/devops/scripts/new/var/result_con_rel.txt
cat /var/log/httpd/error_log| egrep '25/Aug/2017:10:01' >>/root/devops/scripts/new/var/result_con_rel.txt
cat /var/log/rabbitmq/rabbit@ztx-controller-135.log| egrep '25-Aug-2017::10:00' >>/root/devops/scripts/new/var/result_con_rel.txt
cat /var/log/rabbitmq/rabbit@ztx-controller-135.log| egrep '25-Aug-2017::10:01' >>/root/devops/scripts/new/var/result_con_rel.txt
sed -i "s/Aug 25/2017-08-25/" /root/devops/scripts/new/var/result_con_rel.txt 
cat /root/devops/scripts/new/var/result_con_rel.txt |sort -t " " -k2 > /root/devops/scripts/new/var/sort_result.txt