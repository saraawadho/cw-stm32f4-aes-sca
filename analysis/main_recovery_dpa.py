import numpy as np
import matplotlib.pyplot as plt
import h5py
from aes import AES
from tqdm import tqdm

def main():


    AES.test_correctness()


    raise ValueError()



    filepath = 'aes_traces_10k_key_0.hdf5'
    with h5py.File(filepath, 'r') as f:
        key = f["key"][:]
        plaintexts = f["plaintexts"][:,:]
        traces = (f["traces"][:,:5000]).astype(float)
        nb_of_bits = f["traces"].attrs['bits_per_sample']
        traces = (traces - (2**(nb_of_bits-1))) / (2**(nb_of_bits))

    nb_of_samples = traces.shape[1]
    doms = np.zeros((16, 256, nb_of_samples), dtype=float)
    for subkey in tqdm(range(256)):
        sbox_lsbs = np.copy(plaintexts)
        sbox_lsbs ^= np.full(plaintexts.shape, subkey, dtype=np.uint8)
        sbox_lsbs = AES.SBOX[sbox_lsbs] & 0x1
        for i in range(16):
            ind = (sbox_lsbs[:,i] == 1)
            dom = np.mean(traces[ind,:],axis=0) - np.mean(traces[~ind,:], axis=0)
            doms[i,subkey,:] = dom

    for i in range(16):
        plt.plot(np.transpose(doms[i,:,:]))
        plt.xlabel("Time [Samples]")
        plt.ylabel("DoM")
        plt.title("DPA: 256 subkey candidates for S-box {:d}".format(i+1))
        plt.savefig("exercise_dpa_solution_{:d}.png".format(i+1), dpi=300)
        plt.close()

    doms = np.max(abs(doms), axis=2)
    roundkey = np.argmax(doms, axis=1)
    count = np.count_nonzero(key == roundkey)
    print("DPA successfully recovered {:d} out of 16 subkeys.".format(count))
    if (count >= 12) and (count < 16):
        print("A small brute-force search does the rest.")

if __name__ == "__main__":
    main()