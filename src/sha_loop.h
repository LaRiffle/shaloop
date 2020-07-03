void sha256_loop(uint8_t * buffer, int n_values, uint8_t * out);
void sha256_loop_parallel(uint8_t * buffer, int n_values, uint8_t * out, int n_threads);
void sha512_loop(uint8_t * buffer, int n_values, uint8_t * out);
