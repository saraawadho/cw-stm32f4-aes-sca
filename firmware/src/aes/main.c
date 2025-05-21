#include "simpleserial.h"
#include "aes.h"
#include <string.h>

uint8_t key[16];
uint8_t plaintext[16];
uint8_t ciphertext[16];

static uint8_t operand_read(uint8_t* data, uint8_t dlen)
{
    if (dlen != 1) {return 1;}
    switch (data[0]) {
        case 1: {simpleserial_put('r', 16, (uint8_t *) key); break;}
        case 2: {simpleserial_put('r', 16, (uint8_t *) plaintext); break;}
        case 3: {simpleserial_put('r', 16, (uint8_t *) ciphertext); break;}
        default: return 2;
    }
    return 0;
}

static uint8_t operand_write(uint8_t* data, uint8_t dlen)
{
    if (dlen != 17) {return 1;}
    switch (data[0]) {
        case 1: {memcpy(key, &(data[1]), 16); AES128_key_expansion(key); break;}
        case 2: {memcpy(plaintext, &(data[1]), 16); break;}
        case 3: {memcpy(ciphertext, &(data[1]), 16); break;}
        default: return 2;
    }
    return 0;
}

uint8_t encrypt(uint8_t* data, uint8_t dlen)
{
  memcpy(ciphertext, plaintext, 16);
  trigger_high();
  AES128_key_encrypt(ciphertext);
  trigger_low();
  return 0;
}

uint8_t decrypt(uint8_t* data, uint8_t dlen)
{
  memcpy(plaintext, ciphertext, 16);
  trigger_high();
  AES128_key_decrypt(plaintext);
  trigger_low();
  return 0;
}

int main(void)
{
  platform_init();
  init_uart();
  trigger_setup();
  simpleserial_init();
  simpleserial_addcmd('R', 1, operand_read);
  simpleserial_addcmd('W', 17, operand_write);
  simpleserial_addcmd('E', 0, encrypt);
  simpleserial_addcmd('D', 0, decrypt);
  while(1) {
    simpleserial_get();
  }
}