import numpy as np
import matplotlib.pyplot as plt
import h5py
from aes import AES
from tqdm import tqdm

def hamming_weight(x):
    weight = np.zeros(x.shape, dtype=int)
    for i in range(8):
        weight += (x >> i) & 1
    return weight

def pearson_correlation(x, y):
    x_mean = np.mean(x, axis=0)
    x_std = np.std(x, axis=0)
    y_mean = np.mean(y, axis=0)
    y_std = np.std(y, axis=0)
    cov = np.matmul(np.transpose(x - x_mean[np.newaxis, :]), y - y_mean[np.newaxis, :])
    cov /= x.shape[0]
    corrcoef = cov / np.outer(x_std, y_std)
    return corrcoef

def main():
    filepath = 'aes_traces_10k_key_0.hdf5'
    with h5py.File(filepath, 'r') as f:
        key = f["key"][:]
        plaintexts = f["plaintexts"][:,:]
        traces = (f["traces"][:,:5000]).astype(float)
        nb_of_bits = f["traces"].attrs['bits_per_sample']
        traces = (traces - (2**(nb_of_bits-1))) / (2**(nb_of_bits))

    nb_of_samples = traces.shape[1]
    corrcoefs = np.zeros((16, 256, nb_of_samples), dtype=float)
    for subkey in tqdm(range(256)):
        hw = np.copy(plaintexts)
        hw ^= np.full(plaintexts.shape, subkey, dtype=np.uint8)
        hw = hamming_weight(AES.SBOX[hw]).astype(float)
        cc = pearson_correlation(hw, traces)
        corrcoefs[:,subkey,:] = cc

    for i in range(16):
        plt.plot(np.transpose(corrcoefs[i,:,:]))
        plt.xlabel("Time [Samples]")
        plt.ylabel("Pearson's correlation coefficient")
        plt.title("CPA: 256 subkey candidates S-box {:d}".format(i+1))
        plt.savefig("exercise_cpa_solution_{:d}.png".format(i+1), dpi=300)
        plt.close()

    corrcoefs = np.max(abs(corrcoefs), axis=2)
    roundkey = np.argmax(corrcoefs, axis=1)
    count = np.count_nonzero(key == roundkey)
    print("CPA successfully recovered {:d} out of 16 subkeys".format(count))
    if (count >= 12) and (count < 16):
        print("A small brute-force search does the rest.")

if __name__ == "__main__":
    main()