import subprocess
import sys
import numpy as np

def call_image_generation_script(X, Y, HD, output):
    script_path = 'modified_script.py'
    subprocess.run([sys.executable, script_path, "--X", str(X), "--Y", str(Y), "--HD", str(HD), "--output", output])

if __name__ == "__main__":
    # Example lists for X, Y, and HD
    traj_ls = np.load('traj_ls.npy')
    X_ls = traj_ls[0,:]*1.2/40
    Y_ls = traj_ls[1,:]*1.2/40
    HD_ls = [270]
    for i in range(len(X_ls)-1):
        alpha  = np.rad2deg(np.arctan2(Y_ls[i+1]-Y_ls[i], X_ls[i+1]-X_ls[i]))
        if alpha < 0:
            alpha = alpha +360
        HD_ls.append(alpha)
    print('size of traj:', len(X_ls))

    for i, (X_value, Y_value, HD_value) in enumerate(zip(X_ls, Y_ls, HD_ls)):
        output_image_path = f'indx_{i}.png'
        call_image_generation_script(X_value, Y_value, HD_value, output_image_path)
