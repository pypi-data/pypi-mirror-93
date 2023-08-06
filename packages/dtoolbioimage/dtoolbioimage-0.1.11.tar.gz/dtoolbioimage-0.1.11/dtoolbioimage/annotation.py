import numpy as np
import skimage.draw

from dtoolbioimage import Image as dbiImage


class AnnotatedImage(object):

    @classmethod
    def from_image(cls, im):
        self = cls()
        self.im = im.view(dbiImage)
        self.canvas = np.zeros(im.shape)

        return self

    def _repr_png_(self):
        return self.canvas.view(dbiImage)._repr_png_()

    def mark_mask(self, mask, col=(255, 255, 255)):
        self.canvas[np.where(mask)] = col

    def draw_line_aa(self, p0, p1, col):

        # print(f"{self.canvas.shape}, draw {p0} to {p1}")

        r0, c0 = p0
        r1, c1 = p1
        rr, cc, aa = skimage.draw.line_aa(r0, c0, r1, c1)

        try:
            self.canvas[rr, cc] = col
        except IndexError:
            pass

    def draw_disk(self, p, radius, col):
        rr, cc = skimage.draw.disk(p, radius)
        self.canvas[rr, cc] = col

    @property
    def merged_im(self):
        return 0.5 * self.im + 0.5 * self.canvas

    def save(self, filename):
        self.merged_im.view(dbiImage).save(filename)
