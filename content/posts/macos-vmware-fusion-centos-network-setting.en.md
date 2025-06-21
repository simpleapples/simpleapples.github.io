---
date: "2012-10-19T12:39:00+00:00"
title: "MacOS + VMware Fusion: Setting Up CentOS Network"
categories:
  - Mac&Linux
---

After performing a minimal installation of CentOS 6.3 in VMware, I found that the network could not be connected whether VMware was set to shared or bridged mode. I searched online for methods to set up CentOS under VMware Workstation, but they did not apply to VMware Fusion on macOS. After some trial and error, I discovered that configuring the CentOS network under Fusion is quite simple. Here’s how:

1. Set VMware to bridged network mode.
2. Change the network card settings:

   ```bash
   $ vi /etc/sysconfig/network-scripts/ifcfg-eth0
   ```

   Modify the values as follows:

   ```bash
   BOOTPROTO="dhcp" // Use DHCP to configure the IP address  
   ONBOOT="yes" // Enable the device at startup  
   ```

3. Restart the network service:

   ```bash
   $ service network restart
   ```

4. Check the network:

   ```bash
   $ ifconfig
   ```

   Verify whether the device eth0 has been assigned the correct IP and whether the network can be pinged successfully.