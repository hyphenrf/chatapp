/* crc.h
 * vim:set noet sts=0 sw=0 ts=4 tw=80:
 * Copyright (C) 2020 Nile University */

#ifndef CRC_H
#define CRC_H

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

typedef uint8_t byte;
typedef size_t word;

struct crc_spec {
	word poly;
	word init;
	bool refin;
	bool refout;
	bool xorout;
	word check;
};

byte lookup(byte message[static 1], word len);
byte * chksum(byte message[static 1], word msglen, byte *buffer);
bool verify(byte message[static 1], word msglen);

#endif /* !CRC_H */
