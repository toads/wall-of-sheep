# coding:utf-8

"""
This File for change channel or manage iface mode

"""

import subprocess

# from scapy.all import set_iface_monitor, get_iface_mode, get_working_ifaces
from scapy.config import conf
import sh


def set_channel(ifaces, channels):
    """Sets the monitor mode (or remove it) from an interface.
        PLEASE RESTART L2socket TO ENABLE THIS CHANGE!
        PLEASE RESTART L2socket TO ENABLE THIS CHANGE!
        PLEASE RESTART L2socket TO ENABLE THIS CHANGE!
        params:
         - iface: the iwconfig interface
         - channel: the iface channel
        """
    assert len(ifaces) == len(channels)
    for iface, channel in zip(ifaces, channels):
        sh.iwconfig(iface, "channel", channel)

#
# def restart_L2socket(s, bpf=None):
#     iface = s.iface
#     s.close()
#     new_s = conf.L2socket(iface, filter=bpf)
#     return new_s
#
#
# def set_monitor(iface):
#     """set iface monitor"""
#
#     return set_iface_monitor(iface, monitor=1)
#
#
# def set_managed(iface):
#     sh.ifconfig(iface, "down")
#     sh.iw(iface, 'set', 'type', 'managed')
#     sh.ifconfig(iface, "up")
#
#
# def get_mode(iface):
#     return get_iface_mode(iface)
#
#
# def get_working_ifaces():
#     return get_working_if()
