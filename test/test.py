import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from trading_models.utils import GIFMaker

path = "./data/bold.nii.gz"
bold = nib.load(path)
img: np.ndarray = bold.get_fdata()
print(img.shape)
gif = GIFMaker()
nx, ny, nz, nt = img.shape
for t in range(nt):
    plt.imsave("temp.png", img[:, :, nz // 2, t])
    gif.add("temp.png")
gif.save("temp", fps=3)

path = "./data/T1w.nii.gz"
t1w = nib.load(path)
img: np.ndarray = t1w.get_fdata()
print(img.shape)
nx, ny, nz = img.shape
plt.imsave("temp.png", img[:, :, nz // 2])
