#!/bin/bash

source debian/vars.sh
set -x

mkdir -p $DEB_INSTALL_ROOT$_httpd_moddir
install apache2/${upstream_name}.so $DEB_INSTALL_ROOT$_httpd_moddir/

mkdir -p $DEB_INSTALL_ROOT${_sysconfdir}/apache2/conf.modules.d/
cp $SOURCE1 $DEB_INSTALL_ROOT${_sysconfdir}/apache2/conf.modules.d/

mkdir -p $DEB_INSTALL_ROOT${_sysconfdir}/apache2/conf.d/
cp $SOURCE2 $DEB_INSTALL_ROOT${_sysconfdir}/apache2/conf.d/qos.conf

