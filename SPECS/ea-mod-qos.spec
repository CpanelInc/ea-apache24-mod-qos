%global ns_name ea-apache24
%global upstream_name mod_qos
%global debug_package %{nil}
%global nice_name mod-qos

Name: %{ns_name}-%{nice_name}
Version: 11.71
Summary: mod_qos is a quality of service module for the Apache Web Server.

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4556 for more details
%define release_prefix 1
License: Apache License, Version 2.0
Release: %{release_prefix}%{?dist}.cpanel
Group: System Environment/Daemons
Vendor: cPanel, Inc.
URL: https://sourceforge.net/projects/mod-qos/
Source: mod_qos-%{version}.tar.gz
Source1: 100_mod_qos.conf

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pcre-devel
Requires: pcre

BuildRequires: tree
BuildRequires: ea-apache24-devel ea-apr-devel ea-apr-util-devel
Requires: ea-apr ea-apr-util
Requires: ea-apache24

%define apr_lib /opt/cpanel/ea-apr16/lib64
%define apr_include /opt/cpanel/ea-apr16/include

%if 0%{?rhel} > 7
BuildRequires: openssl, openssl-devel
Requires: openssl
%else
BuildRequires: ea-openssl11 >= %{ea_openssl_ver}, ea-openssl11-devel >= %{ea_openssl_ver}
Requires: ea-openssl11 >= %{ea_openssl_ver}
%endif

%description
mod_qos is a quality of service module for the Apache Web Server. It
implements control mechanisms that can provide different priority to different
requests and controls server access based on available resources

%prep
%setup -q -n mod_qos-%{version}

cp %{SOURCE1} .

%build
cd apache2
%define apr_lib /opt/cpanel/ea-apr16/lib64
%if 0%{?rhel} > 7
    %{_httpd_apxs} -L/usr/lib64 -L%{apr_lib} -c mod_qos.c -lcrypto -lpcre -lapr-1 -laprutil-1
%else
    # NOTE: this is for CentOS_7 only

    # OK this is doing quadruple back flips and well I cannot get this done otherwise
    # the normal task is to call apxs, but I could not coerce it to use the rpath I needed
    # so my first choice was to do the outputted libtool commands, but I still could not
    # coerce the rpath.
    #
    # So the final step was to use libtool to compile the code
    # and use the libtool outputted gcc command to link it and then coercing the rpath as
    # we need it.
    #

    mkdir -p .libs
    /opt/cpanel/ea-apr16/lib64/apr-1/build/libtool --verbose --mode=compile gcc -std=gnu99 -prefer-pic -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic  -DLINUX -D_REENTRANT -D_GNU_SOURCE -pthread -I/usr/include/apache2  -I/opt/cpanel/ea-apr16/include/apr-1   -I/opt/cpanel/ea-apr16/include/apr-1 -I/opt/cpanel/ea-openssl11/include  -c -o mod_qos.lo mod_qos.c && touch mod_qos.slo
    gcc -shared  -fPIC -DPIC .libs/mod_qos.o -Wl,-rpath="/opt/cpanel/ea-openssl11/lib:/opt/cpanel/ea-apr16/lib64:/opt/cpanel/ea-apr16/lib64" -L/usr/lib64 -L/opt/cpanel/ea-openssl11/lib -L/opt/cpanel/ea-apr16/lib64 -lcrypto -lpcre /opt/cpanel/ea-apr16/lib64/libaprutil-1.so -lcrypt -lexpat -ldb-5.3 /opt/cpanel/ea-apr16/lib64/libapr-1.so -lpthread -ldl  -Wl,-z -Wl,relro -Wl,-z -Wl,now   -pthread -Wl,-soname -o .libs/mod_qos.so
%endif
mv .libs/%{upstream_name}.so .
strip -g %{upstream_name}.so

%install
set -x
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_httpd_moddir}
mkdir -p %{buildroot}%{_sysconfdir}/apache2/conf.modules.d/

install apache2/%{upstream_name}.so %{buildroot}%{_httpd_moddir}/
install -p 100_mod_qos.conf %{buildroot}%{_sysconfdir}/apache2/conf.modules.d/100_mod_qos.conf

%clean
rm -rf %{buildroot}

%files
%{_libdir}/apache2/modules/mod_qos.so
%config(noreplace) %{_sysconfdir}/apache2/conf.modules.d/100_mod_qos.conf

%changelog
* Fri Mar 11 2022 Julian Brown <julian.brown@cpanel.net> - 11.71-1
- ZC-9726: Initial build

