#!/bin/bash

source debian/vars.sh
set -x

mkdir -p $DEB_INSTALL_ROOT$_httpd_moddir
install apache2/${upstream_name}.so $DEB_INSTALL_ROOT$_httpd_moddir/

