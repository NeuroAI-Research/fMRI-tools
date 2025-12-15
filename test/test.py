import os

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from scipy import ndimage, optimize
from trading_models.utils import GIFMaker


class FMRIData:
    def __repr__(s):
        return f"FMRIData: {s.arr.shape}"

    def __init__(s, path):
        s.path = path
        s.data = nib.load(path)
        s.arr: np.ndarray = s.data.get_fdata()

    def plot(s):
        if len(s.arr.shape) == 4:
            nx, ny, nz, nt = s.arr.shape
            gif = GIFMaker()
            for t in range(nt):
                plt.imsave("temp.png", s.arr[:, :, nz // 2, t])
                gif.add("temp.png")
            gif.save(s.path)
            os.remove("temp.png")
        elif len(s.arr.shape) == 3:
            nx, ny, nz = s.arr.shape
            plt.imsave(f"{s.path}.png", s.arr[:, :, nz // 2])

    def motion_correction(s, inplace=True):
        nx, ny, nz, nt = s.arr.shape
        ref_vol = s.arr[..., nt // 2]

        def affine_trans(vol, params):
            _, trans = params[:3], params[3:]
            return ndimage.affine_transform(vol, np.eye(3), offset=trans, order=1)

        def loss_fn(params, vol):
            new_vol = affine_trans(vol, params)
            return np.mean((new_vol - ref_vol) ** 2)

        new_arr = np.zeros_like(s.arr)
        for t in range(nt):
            vol = s.arr[..., t]
            x0 = np.zeros(6)
            res = optimize.minimize(loss_fn, x0, args=(vol), method="L-BFGS-B")
            new_arr[..., t] = affine_trans(vol, res.x)
            print(
                f"motion_correction MSE@t={t}: {loss_fn(x0, vol)} -> {loss_fn(res.x, vol)}"
            )
        if inplace:
            s.arr = new_arr
        return new_arr


d1 = FMRIData("./data/bold.nii.gz")
print(d1)
# d2 = FMRIData("./data/T1w.nii.gz")
# print(d2)
# d1.plot()
# d2.plot()
d1.motion_correction()
