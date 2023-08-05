''' 
Ntp Genie Ops Object Outputs for Junos.
'''


class NtpOutput(object):

    ShowNtpAssociations = {
       'clock_state': {'system_status': {'associations_address': '172.16.229.65',
                                         'associations_local_mode': 'active',
                                         'clock_offset': 73.819,
                                         'clock_refid': '.GNSS.',
                                         'clock_state': 'synchronized',
                                         'clock_stratum': 1,
                                         'root_delay': 1.436}},
        'peer': {'10.2.2.2': {'local_mode': {'active': {'delay': 1.47,
                                                        'jitter': 52.506,
                                                        'mode': 'falseticker',
                                                        'offset': -46.76,
                                                        'poll': 128,
                                                        'reach': 271,
                                                        'receive_time': 84,
                                                        'refid': '172.16.229.65',
                                                        'remote': '10.2.2.2',
                                                        'stratum': 2,
                                                        'type': 'active'}}},
                '172.16.229.65': {'local_mode': {'active': {'delay': 1.436,
                                                            'jitter': 10.905,
                                                            'mode': 'synchronized',
                                                            'offset': 73.819,
                                                            'poll': 64,
                                                            'reach': 377,
                                                            'receive_time': 59,
                                                            'refid': '.GNSS.',
                                                            'remote': '172.16.229.65',
                                                            'stratum': 1,
                                                            'type': 'active'}}},
                '172.16.229.66': {'local_mode': {'active': {'delay': 0.969,
                                                            'jitter': 8.964,
                                                            'mode': 'final '
                                                                    'selection '
                                                                    'set',
                                                            'offset': 59.428,
                                                            'poll': 64,
                                                            'reach': 377,
                                                            'receive_time': 63,
                                                            'refid': '.GNSS.',
                                                            'remote': '172.16.229.66',
                                                            'stratum': 1,
                                                            'type': 'active'}}},
                '10.145.32.44': {'local_mode': {'active': {'delay': 42.72,
                                                            'jitter': 6.228,
                                                            'mode': 'final '
                                                                    'selection '
                                                                    'set',
                                                            'offset': 64.267,
                                                            'poll': 64,
                                                            'reach': 377,
                                                            'receive_time': 61,
                                                            'refid': '.GNSS.',
                                                            'remote': '10.145.32.44',
                                                            'stratum': 1,
                                                            'type': 'active'}}}}
    }

    ShowNtpStatus = {
        'clock_state': {'system_status': {'clock': 'df981ae8.eb6e7ee8  Thu, Nov 15 2018 11:18:48.919',
                                          'frequency': 4.968,
                                          'jitter': 12.27,
                                          'leap_status': 'leap_none',
                                          'number_of_events': 4,
                                          'offset': 67.812,
                                          'peer': 22765,
                                          'poll': 6,
                                          'precision': -23.0,
                                          'processor': 'amd64',
                                          'recent_event': 'event_peer/strat_chg',
                                          'refid': '172.16.229.65',
                                          'reftime': 'df981acf.bfa97435  Thu, Nov 15 2018 11:18:23.748',
                                          'rootdelay': 1.434,
                                          'rootdispersion': 82.589,
                                          'stability': 0.89,
                                          'state': 4,
                                          'status': '0644',
                                          'stratum': 2,
                                          'synch_source': 'sync_ntp',
                                          'system': 'FreeBSDJNPR-11.0-20171206.f4cad52_buil',
                                          'version': 'ntpd 4.2.0-a Tue Dec 19 '
                                                     '21:12:44  2017 (1)'}}
    }

    ShowConfigurationSystemNtpSet = {
        'vrf': {'default': {'address': {'10.2.2.2': {'isconfigured': {'True': {'address': '10.2.2.2',
                                                                        'isconfigured': True}},
                                              'type': {'peer': {'address': '10.2.2.2',
                                                                'type': 'peer',
                                                                'vrf': 'default'}}}}},
         'mgmt_junos': {'address': {'172.16.229.65': {'isconfigured': {'True': {'address': '172.16.229.65',
                                                                               'isconfigured': True}},
                                                     'type': {'server': {'address': '172.16.229.65',
                                                                         'type': 'server',
                                                                         'vrf': 'mgmt_junos'}}},
                                    '172.16.229.66': {'isconfigured': {'True': {'address': '172.16.229.66',
                                                                               'isconfigured': True}},
                                                     'type': {'server': {'address': '172.16.229.66',
                                                                         'type': 'server',
                                                                         'vrf': 'mgmt_junos'}}},
                                    '10.145.32.44': {'isconfigured': {'True': {'address': '10.145.32.44',
                                                                               'isconfigured': True}},
                                                     'type': {'server': {'address': '10.145.32.44',
                                                                         'type': 'server',
                                                                         'vrf': 'mgmt_junos'}}}}}}
    }

    Ntp_info = {
        'clock_state': {'system_status': {'actual_freq': 4.968,
                                          'associations_address': '172.16.229.65',
                                          'associations_local_mode': 'active',
                                          'clock_offset': 73.819,
                                          'clock_precision': -23.0,
                                          'clock_refid': '.GNSS.',
                                          'clock_state': 'synchronized',
                                          'clock_stratum': 1,
                                          'reference_time': 'df981acf.bfa97435  '
                                                            'Thu, Nov 15 2018 '
                                                            '11:18:23.748',
                                          'root_delay': 1.436,
                                          'root_dispersion': 82.589}},
        'vrf': {'default': {'associations': {'address': {'10.2.2.2': {'local_mode': {'active': {'isconfigured': {'True': {'address': '10.2.2.2',
                                                                                                                          'delay': 1.47,
                                                                                                                          'vrf': 'default',
                                                                                                                          'local_mode': 'active',
                                                                                                                          'isconfigured': True,
                                                                                                                          'offset': -46.76,
                                                                                                                          'poll': 128,
                                                                                                                          'reach': 271,
                                                                                                                          'receive_time': 84,
                                                                                                                          'refid': '172.16.229.65',
                                                                                                                          'stratum': 2}}}}}}},
                            'unicast_configuration': {'address': {'10.2.2.2': {'type': {'peer': {'address': '10.2.2.2',
                                                                                                 'type': 'peer',
                                                                                                 'vrf': 'default'}}}}}},
                'mgmt_junos': {'associations': {'address': {'172.16.229.65': {'local_mode': {'active': {'isconfigured': {'True': {'address': '172.16.229.65',
                                                                                                                                 'delay': 1.436,
                                                                                                                                 'vrf': 'mgmt_junos',
                                                                                                                                 'local_mode': 'active',
                                                                                                                                 'isconfigured': True,
                                                                                                                                 'offset': 73.819,
                                                                                                                                 'poll': 64,
                                                                                                                                 'reach': 377,
                                                                                                                                 'receive_time': 59,
                                                                                                                                 'refid': '.GNSS.',
                                                                                                                                 'stratum': 1}}}}},
                                                            '172.16.229.66': {'local_mode': {'active': {'isconfigured': {'True': {'address': '172.16.229.66',
                                                                                                                                 'vrf': 'mgmt_junos',
                                                                                                                                 'local_mode': 'active',
                                                                                                                                 'delay': 0.969,
                                                                                                                                 'isconfigured': True,
                                                                                                                                 'offset': 59.428,
                                                                                                                                 'poll': 64,
                                                                                                                                 'reach': 377,
                                                                                                                                 'receive_time': 63,
                                                                                                                                 'refid': '.GNSS.',
                                                                                                                                 'stratum': 1}}}}},
                                                            '10.145.32.44': {'local_mode': {'active': {'isconfigured': {'True': {'address': '10.145.32.44',
                                                                                                                                 'vrf': 'mgmt_junos',
                                                                                                                                 'local_mode': 'active',
                                                                                                                                 'delay': 42.72,
                                                                                                                                 'isconfigured': True,
                                                                                                                                 'offset': 64.267,
                                                                                                                                 'poll': 64,
                                                                                                                                 'reach': 377,
                                                                                                                                 'receive_time': 61,
                                                                                                                                 'refid': '.GNSS.',
                                                                                                                                 'stratum': 1}}}}}}},
                               'unicast_configuration': {'address': {'172.16.229.65': {'type': {'server': {'address': '172.16.229.65',
                                                                                                          'type': 'server',
                                                                                                          'vrf': 'mgmt_junos'}}},
                                                                     '172.16.229.66': {'type': {'server': {'address': '172.16.229.66',
                                                                                                          'type': 'server',
                                                                                                          'vrf': 'mgmt_junos'}}},
                                                                     '10.145.32.44': {'type': {'server': {'address': '10.145.32.44',
                                                                                                          'type': 'server',
                                                                                                          'vrf': 'mgmt_junos'}}}}}}}
    }
