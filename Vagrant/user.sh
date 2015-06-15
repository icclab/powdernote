cd devstack

name="username"
password="password"

source keystonerc
keystone user-create --name=$name --pass=$password
keystone tenant-create --name=$name

role_id=`keystone role-list | grep -i -w "admin" | awk '{print($2);}'`
user_id=`keystone user-list | grep -i -w "$name" | awk '{print($2);}'`
tenant_id=`keystone tenant-list | grep -i -w "$name" | awk '{print($2);}'`

keystone user-role-add --role_id=$role_id --tenant_id=$tenant_id --user_id=$user_id

printf "export OS_USERNAME=$name\nexport OS_PASSWORD=$password\nexport OS_TENANT_NAME=$name\nexport OS_AUTH_URL=http://localhost:35357/v2.0" > "newkeystonerc"

source newkeystonerc

tenant_id=`keystone token-get | grep -i "tenant_id" | awk '{print($4);}'`
token=`keystone token-get | grep -i -w "id" | awk '{print($4);}'`

curl -X PUT -i -H "X-Auth-Token:$token" http://10.0.2.15:8080/v1/AUTH_$tenant_id/powdernote-$name
