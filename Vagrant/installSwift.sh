sudo apt-get -y install git
git clone https://github.com/openstack-dev/devstack.git
cd devstack && git checkout stable/juno

printf "[[local|localrc]] \nDEST=/opt/stack\nADMIN_PASSWORD=secrete\nDATABASE_PASSWORD=\$ADMIN_PASSWORD\nRABBIT_PASSWORD=\$ADMIN_PASSWORD\nSERVICE_PASSWORD=\$ADMIN_PASSWORD\nSERVICE_TOKEN=a682f596-76f3-11e3-b3b2-e716f9080d50\n\nLOGFILE=\$DEST/logs/stack.sh.log\nLOGDAYS=1\n\ndisable_all_services\nenable_service key mysql s-proxy s-object s-container s-account\nSWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5\nSWIFT_REPLICAS=1\nSWIFT_DATA_DIR=\$DEST/data/swift\n\nKEYSTONE_BRANCH=stable/juno\nSWIFT_BRANCH=stable/juno" > "local.conf"
./stack.sh

printf "export OS_USERNAME=admin\nexport OS_PASSWORD=secrete\nexport OS_TENANT_NAME=admin\nexport OS_AUTH_URL=http://localhost:35357/v2.0" > "keystonerc"
source keystonerc && serviceId=`keystone service-list | grep -i "swift" | awk '{print($2);}'`

service_id=`keystone service-list | grep -i "swift" | awk '{print($2);}'`
old_endpoint_id=`keystone endpoint-list | grep -i $service_id | awk '{print($2);}'`

keystone endpoint-delete $old_endpoint_id

source keystonerc && keystone endpoint-create \
--region RegionOne \
--service-id=$serviceId \
--publicurl 'http://192.168.33.10:8080/v1/AUTH_$(tenant_id)s' \
--adminurl 'http://10.0.2.15:8080' \
--internalurl 'http://10.0.2.15:8080/v1/AUTH_$(tenant_id)s'
