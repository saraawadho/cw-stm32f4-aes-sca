PLATFORM := CW308_STM32F4
CRYPTO_TARGET := NONE
SS_VER := SS_VER_1_1
TARGET := AES

SRC_DIR := ./src/aes
SRC := $(subst $(SRC_DIR)/,,$(wildcard $(SRC_DIR)/*.c))

OPT := 3

VPATH := :$(SRC_DIR)/
EXTRAINCDIRS := $(SRC_DIR)/
VERBOSE := true

FIRMWAREPATH := ./src/cw308
include $(FIRMWAREPATH)/Makefile.inc