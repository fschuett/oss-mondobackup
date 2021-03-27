#
# Spec file for oss-mondobackup
# Copyright (c) 2016-2021 Frank Schütte <fschuett@gymhim.de> Hildesheim, Germany.  All rights reserved.
#
%if 0%{?sle_version} == 150100 && 0%{?is_opensuse}
%define osstype oss
%else
%define osstype cranix
%endif
Name:		oss-mondobackup
Summary:	OSS mondo backup scripts
Version:	7.0
Release:	1.1
License:	GPL-3.0-or-later
Vendor:		openSUSE Linux
Group:		Productivity/Archiving
Source:		%{name}-%{version}.tar.gz

Requires:	%{osstype}-base
Requires:	bash mondo mindi mindi-busybox screen
Requires:	perl-Net-IPv4Addr
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(systemd) >= 197
Requires:   /usr/bin/xz
%{?systemd_ordering}

BuildRoot:    %{_tmppath}/%{name}-root

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
mkdir -p %{buildroot}%{_fillupdir}
install -m 644 sysconfig.%{name} %{buildroot}%{_fillupdir}/sysconfig.%{name}

cp -R etc/* %{buildroot}/etc/
mkdir -p %{buildroot}/sbin
cp -R sbin/* %{buildroot}/sbin/

for f in `ls *.service *.timer`; do
  install -D -m 0644 ${f} %{buildroot}%{_unitdir}/${f}
done

%pre
#only the timer can be enabled/disabled/masked !
%service_add_pre %{name}-full.service %{name}-full.timer %{name}-diff.service %{name}-diff.timer %{name}-inc.service %{name}-inc.timer

%post
%service_add_post %{name}-full.service %{name}-full.timer %{name}-diff.service %{name}-diff.timer %{name}-inc.service %{name}-inc.timer
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

%preun
%service_del_preun %{name}-full.service %{name}-full.timer %{name}-diff.service %{name}-diff.timer %{name}-inc.service %{name}-inc.timer

%postun
%service_del_postun %{name}-full.service %{name}-full.timer %{name}-diff.service %{name}-diff.timer %{name}-inc.service %{name}-inc.timer

%files
%defattr(644,root,root,755)
%dir /etc/mindi
/etc/mindi/mindi.conf.in
%{_fillupdir}/sysconfig.%{name}
%attr(755,root,root) /sbin/%{name}
%attr(755,root,root) /sbin/rc%{name}
%{_unitdir}/%{name}-full.service
%{_unitdir}/%{name}-full.timer
%{_unitdir}/%{name}-diff.service
%{_unitdir}/%{name}-diff.timer
%{_unitdir}/%{name}-inc.service
%{_unitdir}/%{name}-inc.timer

%changelog

