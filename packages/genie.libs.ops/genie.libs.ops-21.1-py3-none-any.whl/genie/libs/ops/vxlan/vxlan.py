# Genie
from genie.ops.base import Base


class Vxlan(Base):
    exclude = ['bytesrecvd',
               'bytessent',
               'capabilitiesrecvd',
               'capabilitiessent',
               'connsdropped',
               'connsestablished',
               'elapsedtime',
               'fd',
               'keepalive',
               'keepaliverecvd',
               'keepalivesent',
               'lastread',
               'lastwrite',
               'msgrecvd',
               'msgsent',
               'neighbortableversion',
               'notificationssent',
               'opensrecvd',
               'openssent',
               'tableversion',
               'remoteport',
               'rtrefreshsent',
               'updatesrecvd',
               'updatessent',
               'prefixversion',
               'tx_id',
               'uptime',
               'up_time',
               'localport',
               'resetreason',
               'resettime',
               'client_nfn',
               'pathnr',
               'bestpathnr',
               'peer_id',
               'bytesattrs',
               'memoryused',
               'prefixreceived',
               'numberattrs',
               'advertisedto',
               'totalnetworks',
               'totalpaths',
               'flags',
               'index',
               'total_mem',
               'memory',
               'total_memory',
               'mac',
               'mac_ip',
               'oif_index',
               '(0.0.0.0.*)',
               'prefix',
               'objects',
               'total_obj',
               'table_version',
               'l2_oiflist_index',
               'num_of_oifs',
               'oifs',
               'numof_converged_tables',
               'rmac',
               'vmac',
               'local_rmac',
               'router_mac',
               'rpf_ifname']