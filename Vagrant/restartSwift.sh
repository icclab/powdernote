vagrant up
vagrant ssh -c "sudo mount -t xfs -o loop,noatime,nodiratime,nobarrier,logbufs=8 /opt/stack/data/swift/drives/images/swift.img /opt/stack/data/swift/drives/sdb1"

vagrant ssh -c "cd devstack && ./rejoin-stack.sh"
