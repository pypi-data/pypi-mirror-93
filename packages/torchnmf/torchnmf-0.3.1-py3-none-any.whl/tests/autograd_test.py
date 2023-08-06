import torch
import librosa
import numpy as np
import matplotlib.pyplot as plt
from librosa import display
from scipy.io import loadmat
from torchnmf.plca import PLCA, SIPLCA, SIPLCA2, SIPLCA3
from torchnmf.nmf import NMF, NMFD, NMF2D, NMF3D
from time import time

torch.set_flush_denormal(True)


def read_bach10_F0s(F0):
    f = np.round(loadmat(F0)['GTF0s'] - 21).astype(int)
    index = np.where(f >= 0)
    pianoroll = np.zeros((88, f.shape[1]))
    for i, frame in zip(index[0], index[1]):
        pianoroll[f[i, frame], frame] = 1
    return pianoroll


if __name__ == '__main__':

    V = torch.rand(100, 1, 64, 64)
    model = NMF2D(V.shape, (32, 32), 8).cuda()
    print(model.H.shape)
    model.fit(V.cuda(), verbose=1)

    exit()
    y, sr = librosa.load('Amen-break.wav', sr=None)

    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    # S = librosa.feature.melspectrogram(y, sr, n_fft=4096, n_mels=256, power=1).astype(np.float32)
    # S = np.stack((S, S), 0)
    S = torch.tensor(S)
    R = 3
    win = (200, 10)
    max_iter = 500

    #net = SIPLCA(S.shape, rank=R, T=20).cuda()
    net = NMFD(S.shape, rank=4, T=20).cuda()

    # W = torch.exp(-torch.arange(64.)).view(1, 1, 64, 1)
    # W /= W.sum()

    niter, V, *_ = net.fit_transform(S.cuda(), sparse=True, verbose=True, max_iter=max_iter, beta=1, sW=0.3)
    net.sort()
    W = net.W.detach().cpu().numpy().reshape(S.shape[0], -1)
    H = net.H.detach().cpu().numpy()

    #print(net.Z.detach().cpu().numpy())

    plt.subplot(3, 1, 1)
    # plt.plot(W[:, 0])
    display.specshow(librosa.amplitude_to_db(W, ref=np.max), y_axis='log', sr=sr)
    plt.title('Template ')
    plt.subplot(3, 1, 2)
    display.specshow(H, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title('Activations')
    plt.subplot(3, 1, 3)
    display.specshow(librosa.amplitude_to_db(V.detach().cpu().numpy(), ref=np.max), y_axis='log', x_axis='time', sr=sr)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Reconstructed spectrogram')
    plt.tight_layout()
    plt.show()
