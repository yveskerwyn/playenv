NAS

https://github.com/Jumpscale/ays_g8_nas/blob/master/blueprints/1_g8_nas.yaml

g8client__gig:
    g8.url: 'gig.demo.greenitglobe.com'
    g8.login: 'yves'
    g8.password: ''
    g8.account: 'Account of Yves'

vdcfarm__nasfarm:

vdc__vdc4nas:
    vdcfarm: 'nasfarm'
    g8.client.name: 'gig'
    g8.location: 'du-conv-1'

node.ovc__nasvm:
    os.image: 'ubuntu 16.04 x64'
    disk.size: 10
    datadisks:
        - 'name:disk1 size:50 type:normal'
        - 'name:disk2 size:50 type:normal'
    os.size: 2
    ports:
        - '139:139'
        - '445:445'
        - '137:137'
        - '138:138'
    vdc: 'vdc4nas'

os.ssh.ubuntu__nasvm_ssh:
    node: 'nasvm'
    aysfs: false
    authorized_keys:
        - ""

user.os__yves:
    password: 'ifilebugs'
    os: nasvm_ssh


blockdevice.raid__nasvm_raid:
    os: 'nasvm_ssh'
    disks:
        - 'disk1'
        - 'disk2'
    raid: 0

mount__nasvm_nas:
    blockdevice: 'nasvm_raid'
    filesystem: 'ext4'
    location: '/var/nas'
    options: 'rw'
    os: 'nasvm_ssh'
        
share.samba__nasvm_samba:
    mount: 'nasvm_nas'
    users:
        - 'yves'

# share.sftp__main:
#     blockdevice: 'vm_share'
#     filesystem: 'ext4'
#     mount:
#         location: '/var/nas'
#         options: 'ro'
#     users:
#         - 'geert'
#         - 'azmy'