#!/bin/bash

source debian/vars.sh
set -x

# pulled from apr-util
mkdir -p config
cp $ea_apr_config config/apr-1-config
cp $ea_apr_config config/apr-config
cp /usr/share/pkgconfig/ea-apr16-1.pc config/apr-1.pc
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config/apr-util-1.pc
cp /usr/share/pkgconfig/ea-apr16-1.pc config
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:`pwd`/config"

cd apache2
apr_lib=/opt/cpanel/ea-apr16/lib64
# Ubuntu 26.04+ dropped libpcre3; use libpcre2-posix instead.
UBUNTU_VERSION=$(. /etc/os-release 2>/dev/null && echo "${VERSION_ID:-0}" | tr -d '.')
if [[ "${UBUNTU_VERSION:-0}" -ge 2604 ]]; then
    ${_httpd_apxs} -L/usr/lib64 -L${apr_lib} -c mod_qos.c -lcrypto -lpcre2-posix -lapr-1 -laprutil-1
else
    ${_httpd_apxs} -L/usr/lib64 -L${apr_lib} -c mod_qos.c -lcrypto -lpcre -lapr-1 -laprutil-1
fi
mv .libs/${upstream_name}.so .
strip -g ${upstream_name}.so

