from torchaudio import load
import numpy as np
import torch
import matplotlib.pyplot as plt

from torchnmf.nmf import NMF as torchNMF

from sklearn.decomposition import NMF
from time import time

torch.set_flush_denormal(True)
# torch.set_default_tensor_type(torch.DoubleTensor)

if __name__ == '__main__':
    duration = 60
    y, sr = load('/media/ycy/Shared/Datasets/MAPS/ENSTDkCl/MUS/MAPS_MUS-alb_se2_ENSTDkCl.wav', normalization=True)
    y = y.mean(0)[:duration * sr]
    windowsize = 2048
    S = torch.stft(y, windowsize, window=torch.hann_window(windowsize)).pow(2).sum(2).sqrt()
    R = 88
    max_iter = 100
    tol = 1e-4

    betas = [0, 0.5, 1, 1.5, 2]
    sk = []
    tch = []
    tchcuda = []

    Snumpy = S.numpy()
    S = S.t()
    Scuda = S.cuda()

    net = torchNMF(S.shape, rank=R)

    for b in betas:
        print('beta =', b)
        model = NMF(R, solver='mu', max_iter=max_iter, beta_loss=b, tol=tol, verbose=True)
        start = time()
        model.fit(Snumpy)
        rate = (time() - start) / model.n_iter_
        print('sklearn', rate)
        sk.append(rate)

        net.cpu()
        start = time()
        niter = net.fit(S, max_iter=max_iter, beta=b, tol=tol, verbose=True)
        rate = (time() - start) / niter
        print('torch', rate)
        tch.append(rate)

        net.cuda()
        start = time()
        niter = net.fit(Scuda, max_iter=max_iter, beta=b, tol=tol, verbose=True)
        rate = (time() - start) / niter
        print('torch + cuda', rate)
        tchcuda.append(rate)

    plt.bar(np.array(betas) - 0.15, sk, width=0.15, align='center', label='sklearn')
    plt.bar(betas, tch, width=0.15, align='center', label='torch')
    plt.bar(np.array(betas) + 0.15, tchcuda, width=0.15, align='center', label='torch+cuda')
    plt.xlabel(r'$\beta$')
    plt.ylabel("Time per Iteration (s)")
    plt.yscale('log')
    plt.legend()
    plt.title('Runtime Benchmark, target matrix size is %d x %d, %d components' % (S.shape[1], S.shape[0], R))
    plt.xticks(betas, [str(i) for i in betas])
    plt.show()
