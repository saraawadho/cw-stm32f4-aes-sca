from teledynelecroyscope import TeledyneLeCroyScope
from CW308_AES import CW308_STM32F4_AES
import numpy as np
import h5py
from tqdm import tqdm
import time

def main():
    filepath = 'traces.hdf5'
    nb_of_samples = 4_900_000
    nb_of_traces = 50

    #scope = TeledyneLeCroyScope(int16_not_int8=True, float_not_int=False)
    cw308 = CW308_STM32F4_AES()
    cw308.test_correctness()

    #cw308.write_hash(cw308.random_32_bytes())
    #secret_scalar_k = cw308.random_32_bytes_with_order_check()
    #cw308.write_secret_scalar_k(secret_scalar_k)

    #with h5py.File(filepath, 'w') as f:
    #    f.create_dataset("trigger", shape=(nb_of_samples), dtype=np.int16)
    #    f.create_dataset("power", shape=(nb_of_traces, nb_of_samples), dtype=np.int16)
    #    f.create_dataset("scalar_k", shape=(32), dtype=np.uint8)
    #    f["scalar_k"][:] = np.frombuffer(secret_scalar_k, dtype=np.uint8)
    #    print('Collecting traces...')
    #    for i in tqdm(range(nb_of_traces)):
    #        scope.arm_single_trace()
    #        time.sleep(0.5)
    #        cw308.sign()
    #        time.sleep(0.5)
    #        f["power"][i,:] = scope.get_single_trace(channel='C3', nb_of_samples = nb_of_samples)
    #    f["trigger"][:] += scope.get_single_trace(channel='C1', nb_of_samples = nb_of_samples)

if __name__ == '__main__':
    main()