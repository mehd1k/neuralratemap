from south_white_L import B, N, F, W, H, MAZE_ID, light_scale  # load the setup of environment
from panda3d.core import GeoMipTerrain, loadPrcFileData, AmbientLight, WindowProperties,GraphicsOutput
from panda3d.core import GraphicsEngine, FrameBufferProperties, Texture, GraphicsPipe
from panda3d.core import Point3, Vec3, Lens, Camera, PerspectiveLens, NodePath
import pathlib
import os
import numpy as np
from scipy.io import savemat

def generate_image(X, Y, HD, output_filename):
    Z = F + 20  # camera is 2cm above the floor
    P = 0
    v_peak = 130
    yaw_sd = 340
    cam_far = 3000  # see 0.8m far; 2000 for previous simulations
    VX, VY = 150, 90
    map_file_path = 'C:\\Users\\mahdi\\Desktop\\yanbo_code'
    map_img = map_file_path + os.sep + f"{MAZE_ID}.png"
    map_img = pathlib.PurePosixPath(pathlib.Path(map_img))
    cmap_img = map_file_path + os.sep + f"c{MAZE_ID}.png"
    cmap_img = pathlib.PurePosixPath(pathlib.Path(cmap_img))
    loadPrcFileData('', 'win-size {} {}'.format(VX, VY))
    MAZE_OUT = output_filename

    # The current position and head direction
    n = 1
    y = Y * np.ones((n,))
    x = X * np.ones((n,))
    hd = HD * np.ones((n,))

    nx = np.maximum(B, np.minimum((x - (W + 1) / 2000) * 1000 + N / 2, B + W - 1))
    ny = np.maximum(B, np.minimum((y - (W + 1) / 2000) * 1000 + N / 2, B + W - 1))
    nhd = (hd - 90) % 360

    # Set up Panda3D
    loadPrcFileData('', 'window-type offscreen')
    loadPrcFileData('', 'win-size {} {}'.format(VX, VY))
    from direct.showbase.ShowBase import ShowBase

    class MyApp(ShowBase):
        def __init__(self):
            ShowBase.__init__(self)
            self.disableMouse()
            
            # Set up the terrain
            terrain = GeoMipTerrain("ratMaze")
            terrain.setHeightfield(map_img)
            terrain.setColorMap(cmap_img)
            terrain.setBruteforce(True)
            root = terrain.getRoot()
            root.setSz(H + F)
            terrain.generate()
            root.reparentTo(self.render)

            # Set up the camera
            self.cam.setPos(nx[0], ny[0], Z)
            self.cam.setHpr(nhd[0], P, 0)
            self.camLens.setFov(VX, VY)
            self.camLens.setFar(cam_far)

            # Set up the lighting
            alight = AmbientLight('alight')
            alight.setColor((light_scale, light_scale, light_scale, 1))
            alnp = self.render.attachNewNode(alight)
            alnp.setPos(N // 2, N // 2, 2000)
            self.render.setLight(alnp)

            # Set up the offscreen buffer
            fb_props = FrameBufferProperties()
            fb_props.setRgbColor(True)
            fb_props.setAlphaBits(1)
            fb_props.setDepthBits(1)
            self.buffer = self.graphicsEngine.makeOutput(
                self.pipe, "offscreen buffer", -2,
                fb_props, WindowProperties.size(VX, VY),
                GraphicsPipe.BFRefuseWindow)

            self.texture = Texture()
            self.buffer.addRenderTexture(self.texture, GraphicsOutput.RTMCopyRam)

            # Render a frame
            self.graphicsEngine.renderFrame()
            image = self.texture.getRamImageAs("RGB")
            image = np.frombuffer(image, np.uint8).reshape((VY, VX, 3))

            import matplotlib.pyplot as plt
            plt.imsave('cimage.png', image)
            # Save the image data
            savemat(f"{MAZE_OUT}.mat",
                    {'images_data': image[:, :, 2].flatten(),
                     'positions_data': np.vstack((X, Y)).T,
                     'hds_data': HD})

            self.buffer.clearRenderTextures()
            self.graphicsEngine.removeWindow(self.buffer)
            self.userExit()

    app = MyApp()
    app.run()

if __name__ == '__main__':
    # Example usage:
    generate_image(0.6, 0.3, 90, "current2_image2")
