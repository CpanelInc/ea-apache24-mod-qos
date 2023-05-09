OBS_PROJECT := EA4
OBS_PACKAGE := ea-apache24-mod-qos
DISABLE_BUILD := arch=i586 repository=CentOS_6.5_standard
DISABLE_DEBUGINFO := repository=CentOS_7 repository=CentOS_8 repository=CentOS_9
include $(EATOOLS_BUILD_DIR)obs.mk
