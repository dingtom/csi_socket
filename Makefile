KERNEL = $(strip $(shell uname -r))
KERNEL_SOURCE = /lib/modules/$(KERNEL)/build

ifneq ($(wildcard $(KERNEL_SOURCE)/include/uapi),)
        KERNEL_HEADERS = $(KERNEL_SOURCE)/include/uapi
else ifneq ($(wildcard $(KERNEL_SOURCE)/include),)
        KERNEL_HEADERS = $(KERNEL_SOURCE)/include
else
        $(error Kernel headers not found)
endif

CFLAGS = -Wall -Werror
LDLIBS = -lm
CC = gcc

log_to_file:log_to_file.c iwl_connector.h
	${CC} ${CFLAGS} log_to_file.c ${LDLIBS} -o log_to_file

iwl_connector.h: connector_users.h

connector_users.h: $(KERNEL_HEADERS)/linux/connector.h
	echo "#undef CN_NETLINK_USERS" > connector_users.h
	grep "#define CN_NETLINK_USERS" $(KERNEL_HEADERS)/linux/connector.h >> connector_users.h

clean:
	rm -f *.o log_to_file.so connector_users.h
