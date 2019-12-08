import numpy as np

src_pt = [360, 3]
calibrate_points = np.float32(
    [[0, 0], [640, 0], [0, 480], [640, 480]])
src_pts = np.float32([src_pt, src_pt, src_pt, src_pt])
check_array = calibrate_points - src_pts
squ = np.square(check_array)
su = np.sum(squ, axis=1)
print(squ)
print(su)
print(np.argmin(su))
