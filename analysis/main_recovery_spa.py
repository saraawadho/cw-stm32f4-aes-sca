import numpy as np
import matplotlib.pyplot as plt
import h5py

def main():
    filepath = 'aes_traces_10k_key_0.hdf5'
    with h5py.File(filepath, 'r') as f:
        key = f["key"][:]
        plaintexts = f["plaintexts"][:,:]
        ciphertexts = f["ciphertexts"][:,:]
        traces = (f["traces"][:,:]).astype(float)
        nb_of_bits = f["traces"].attrs['bits_per_sample']
        traces = (traces - (2**(nb_of_bits-1))) / (2**(nb_of_bits))

    plt.plot(traces[5,:])
    plt.xlabel("Time [Samples]")
    plt.ylabel("Power consumption")
    plt.title("A single trace")
    plt.savefig("exercise_spa_solution_1.png", dpi=300)
    plt.close()

    traces_mean = np.mean(traces, axis=0)
    plt.plot(traces_mean)
    plt.xlabel("Time [Samples]")
    plt.ylabel("Power consumption")
    plt.title("Mean trace")
    plt.savefig("exercise_spa_solution_2.png", dpi=300)
    plt.close()

    print("In the mean trace, a pattern with 10 repetitions is clearly visible.")
    print("It is reasonable to assume that these are the 10 AES-encryption rounds.")
    print("For first- and last-round attacks, only a small part of the matrix of traces needs to be retained.")
    print("This way, fewer computations have to be performed.")

if __name__ == "__main__":
    main()