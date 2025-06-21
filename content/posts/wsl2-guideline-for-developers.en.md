---
date: "2020-06-01T19:02:00+00:00"
title: "WSL2 Installation Guide for Developers"
categories:
  - DevOps
---

### Why Use Windows for Development

For a long time, macOS has been favored by programmers for its Unix-like features. However, in recent years, Apple has rarely introduced groundbreaking hardware products. The removal of the Esc key, the use of butterfly keyboards, almost zero hardware upgradability, and tightened system permissions have made Macs less suitable for programming than before. On the other hand, the PC ecosystem has maintained software openness while its hardware experience has gradually caught up with or even surpassed Macs. I no longer want to use a Mac for development and a PC for gaming; I hope to use one computer for both gaming and development, so I've returned to the PC camp.

With Microsoft's embrace of the open-source community, Windows has also become more programmer-friendly. After the release of Windows 10 version 2004, WSL2 can be used in the official version of Windows 10. Unlike macOS, WSL2 provides a native Linux environment rather than a Unix-like one, and you can even choose your preferred distribution from the App Store. Compared to WSL1, WSL2 uses Hyper-V virtualization, solving issues like the inability to install Docker on WSL1.

### WSL1 vs. WSL2

Compared to WSL1, WSL2 offers a more complete Linux kernel through virtualization, but this approach also introduces some issues. Microsoft provided the following chart to illustrate these differences:

![](/images/20200601_01.png)

The point that WSL2 cannot run simultaneously with VMware Workstation and VirtualBox is outdated. Both VirtualBox and VMware Workstation have released new versions supporting WSL2 and Hyper-V.

WSL2's cross-OS disk performance is indeed frustratingly low, especially for small files. Installing a Python dependency might take several minutes, and installing a NodeJS dependency... let's not even go there. There are countless complaints under the related issue, but no one has solved it yet, as seen here: [https://github.com/microsoft/WSL/issues/4197](https://github.com/microsoft/WSL/issues/4197). However, Microsoft mentions in their documentation that there are many ways to avoid using the file system across OS, such as using VSCode's remote deployment feature, which I believe is a better practice and have adopted myself. Of course, if you must use the file system across OS, it's better to stay with WSL1 (WSL1 is too weak, better stick with VirtualBox).

Besides what's mentioned in the table, I think the biggest issue with WSL2 is... it consumes too many resources. My computer has 16GB of RAM, and after using WSL2, it consumes 11GB of memory right after booting. Although you can use `wsl --shutdown` to close the virtual machine and free up resources, WSL2's resource consumption is almost double compared to VirtualBox and WSL1.

> Microsoft provides a way to limit WSL2 resources, see [https://docs.microsoft.com/en-us/windows/wsl/release-notes#build-18945](https://docs.microsoft.com/en-us/windows/wsl/release-notes#build-18945)

### What to Do

Now that we understand what WSL2 is, the next question is how to proceed. This article will guide you through the following installation process:

- Upgrade Windows 10 to version 2004
- Enable WSL2 and install Linux

And some best practices:

- Network interoperability
- File system interoperability
- Using Docker

Finally, we'll discuss the future of WSL2.

### Upgrading to Windows 10 2004

There are several ways to upgrade to Windows 10 version 2004. The most reliable method is through Settings - Update & Security for an OTA upgrade. However, Windows updates are rolled out in batches, and the 2004 update might not appear in your update interface for a month or two.

A quicker method is to download the image from the official site and upgrade. Visit this link to download and run the upgrade to the latest version: [https://www.microsoft.com/software-download/windows10](https://www.microsoft.com/software-download/windows10). Note that there may be more bugs in the initial release, so if you mind, you might want to wait a bit.

### Enabling WSL2

The process of upgrading Windows 10 shouldn't pose too many issues. After upgrading, you'll need to configure some settings to use WSL2. First, enable the Windows Subsystem for Linux feature by opening a PowerShell window with administrator privileges and entering the following command, then restart the system:

```PowerShell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

After restarting, Windows defaults to WSL1. You'll also need to enable the Virtual Machine Platform feature by entering the following command in PowerShell, then restart the system again:

```PowerShell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

After restarting, enter the following command in PowerShell to set the default WSL version to WSL2:

```PowerShell
wsl --set-default-version 2
```

Next, find a Linux distribution in the Microsoft Store to install. After installation, execute `wsl -l -v` in PowerShell to see if the current distribution is running on WSL2. If it shows version 1... please repeat the installation steps above.

> If you encounter errors setting the WSL version to WSL2, visit [https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel](https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel) to download the WSL2 Kernel.

### Network Interoperability

WSL2 does not share a localhost with Windows, so unlike WSL1, Linux and Windows do not have seamless network interoperability.

Windows can access network services started by WSL2 using localhost directly, but Linux cannot access network services started by Windows this way. You can use the following script to get Windows' IP and access Windows using the IP:

```bash
ip route | grep default | awk '{print $3}'
```

### File System Interoperability

WSL2 accesses the Windows file system by mounting partitions, with Windows disks mounted under `/mnt`, such as `/mnt/c`.

Compared to WSL1, this time Windows can also access Linux partitions. You can enter `\\wsl$\<subsystem name>` in File Explorer to access the corresponding subsystem partition. For convenience, you can also mount the Linux partition as a disk in File Explorer.

A more convenient way is to use `explorer.exe .` in the Terminal to directly open the current directory in File Explorer, similar to `open .` on Mac.

### Using Docker

WSL2 brings a complete Linux kernel, so you can install Docker following the Linux installation process and use it normally. However, there is a minor issue. WSL2's systemd is not yet native, meaning the issue of not being able to start service daemons, which existed on WSL1, still persists, and Docker services are no exception.

There are three solutions to this problem:

- You can have Windows execute a startup script to start Docker in WSL2. See [https://blog.csdn.net/XhyEax/article/details/105560377](https://blog.csdn.net/XhyEax/article/details/105560377). This solution existed in the WSL1 era, and I have used it without encountering issues.

- The second solution is to use a third-party tool to run systemd. See [https://github.com/arkane-systems/genie](https://github.com/arkane-systems/genie), which provides a separate namespace to run systemd.

- The third solution is to use Docker Desktop. Versions 2.3.0.2 and above already support WSL2 and Hyper-V, saving some hassle.

### GPU Support

At Build 2020, it was announced that WSL2 would support GPUs, and Nvidia released a preview version of CUDA on WSL2, available here: [https://developer.nvidia.com/cuda/wsl](https://developer.nvidia.com/cuda/wsl).

This means that in the future, you can use GPU acceleration to train models directly on Windows. Although support is still limited, it's already a significant step ahead compared to Mac.

### Conclusion

In terms of architecture, WSL2 doesn't offer major innovations; it's essentially a virtual machine running on Hyper-V. You can achieve 100% of its functionality with VMware Workstation or VirtualBox through simple configurations, with better performance and less resource consumption. However, WSL2, being a native feature, offers convenience and compatibility in configuration, greatly reducing the effort users spend on setup and achieving maximum out-of-the-box usability. This has been a major reason why Apple has consistently attracted developers. At this point, using Windows + WSL2 to build a development environment can meet most needs.

### References

https://github.com/microsoft/WSL/issues/4197

https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel

https://docs.microsoft.com/en-us/windows/wsl/install-win10

https://github.com/arkane-systems/genie

https://docs.microsoft.com/en-us/windows/wsl/release-notes#build-18945

https://developer.nvidia.com/cuda/wsl

https://devblogs.microsoft.com/directx/directx-heart-linux/