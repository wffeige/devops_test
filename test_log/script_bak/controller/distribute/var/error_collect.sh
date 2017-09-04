> /root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/keystone/keystone.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/ceph/ceph.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/ceph/ceph.audit.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/ceph/ceph-mon.ztx-controller-136.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/glance/registry.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/glance/api.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/cinder/cinder-manage.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/cinder/volume.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/cinder/api.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/cinder/scheduler.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/nova/nova-scheduler.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/nova/nova-conductor.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/nova/nova-cert.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/nova/nova-api.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/nova/nova-consoleauth.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/nova/nova-novncproxy.log >>/root/devops/scripts/controller/distribute/var/result.txt
awk -F " " '{if ($1=="2017-08-24" &&   $2>="03:00:00" && $2<="13:30:00"  && $4 =="ERROR") print $0}' /var/log/neutron/server.log >>/root/devops/scripts/controller/distribute/var/result.txt
cat /var/log/rabbitmq/rabbit@ztx-controller-136.log|grep '24-Aug-2017'|grep ERROR  >>/root/devops/scripts/controller/distribute/var/result.txt
cat /root/devops/scripts/controller/distribute/var/result.txt |sort -t " " -k2 > /root/devops/scripts/controller/distribute/var/sort_result.txt