> /root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/keystone/keystone-tokenflush.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/keystone/keystone.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/ceph/ceph.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/ceph/ceph.audit.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/ceph/ceph-mon.ztx-controller-136.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/cinder-manage.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/volume.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/api.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/cinder/scheduler.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-scheduler.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-conductor.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-manage.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-cert.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-api.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-consoleauth.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/nova/nova-novncproxy.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="10:00:00" && $2<="10:01:00" ) print $0}' /var/log/neutron/server.log >>/root/devops/scripts/compute/guanlian/var/result.txt
awk -F " " '{if ($1=="Aug" && $2=="24" &&$3>="10:00:00" && $3<="10:01:00") print $0}' /var/log/messages >>/root/devops/scripts/compute/guanlian/var/result.txt
sed -i "s/Aug 24/2017-08-24/" /root/devops/scripts/compute/guanlian/var/result.txt 
cat /root/devops/scripts/compute/guanlian/var/result.txt |sort -t " " -k2 > /root/devops/scripts/compute/guanlian/var/tmp.txt