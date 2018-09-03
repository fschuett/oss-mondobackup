#
# Spec file for oss-mondobackup
# Copyright (c) 2016 Frank Schütte <fschuett@gymhim.de> Hildesheim, Germany.  All rights reserved.
#
Name:		oss-mondobackup
Summary:	OSS mondo backup scripts
Version:	7.0
Release:	1.1
License:	GPLv3
Vendor:		openSUSE Linux
Packager:	fschuett@gymhim.de
Group:		Productivity/
Source:		%{name}-%{version}.tar.gz

Requires:	oss-base
Requires:	bash mondo mindi mindi-busybox screen

BuildRoot:    %{_tmppath}/%{name}-root
Requires:	oss-base

%description
This package provides a backup script to create mondorestore images for full automatic server restore.

Authors:
--------
        Frank Schütte

%prep
%setup -D

%build
# nothing to do

%install
# install files and directories
mkdir -p %{buildroot}/var/adm/fillup-templates
install -m 644 -o root -g root sysconfig.%{name} %{buildroot}/var/adm/fillup-templates/sysconfig.%{name}

mkdir -p %{buildroot}/sbin %{buildroot}/etc/cron.d
cp -R etc/* %{buildroot}/etc/
cp -R sbin/* %{buildroot}/sbin/

%post
# setup rights
if [ -d /home/sysadmins/administrator ]
then
   DATE=`date +%Y-%m-%d:%H-%M`
   MINDI=/etc/mindi/mindi.conf
   if [ -e $MINDI ]; then
     cp $MINDI $MINDI.$DATE
   fi
   cp $MINDI.in $MINDI
fi

%fillup_only
exit 0

%files
%defattr(-,root,root)
/etc/cron.d/oss-mondobackup
/etc/mindi/mindi.conf.in
/var/adm/fillup-templates/sysconfig.%{name}
/sbin/oss-mondobackup
/sbin/oss-mondobackup-diff-full

%changelog

