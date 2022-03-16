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
    %{_httpd_apxs} -L/usr/lib64 -L/opt/cpanel/ea-openssl11/lib -L%{apr_lib} -c mod_qos.c -lcrypto -lpcre -lapr-1 -laprutil-1
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

