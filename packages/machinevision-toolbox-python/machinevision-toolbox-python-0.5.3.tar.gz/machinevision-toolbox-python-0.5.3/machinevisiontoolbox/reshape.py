"""
hcat
vcat
grid(shape=(), list or *pos)

scale(factor, width, height)
rotate
reduce(factor, width, height)
warp
affinemap

pad(halign="<^>", valign="^v-", align="<|>v^-, width=, height=)

samesize by scaling and padding
"""

import numpy as np

class ReshapeMixin:

    @classmethod
    def hcat(cls, *pos, pad=0):

        if isinstance(pos[0], (tuple, list)):
            images = pos[0]
        else:
            images = pos
        
        height = max([image.height for image in images])

        combo = np.empty(shape=(height,0))

        u = []
        for image in images:
            if image.height < height:
                image = np.pad(image.image, ((0,height-image.height),(0,0)), constant_values=(pad,0))
            else:
                image = image.image
            u.append(combo.shape[1])
            combo = np.hstack((combo, image))
        
        return cls(combo), u

    def pad(self, left=0, right=0, top=0, bottom=0, value=0):

        pw = ((top,bottom),(left,right))
        const = (value, value)

        return self.__class__(np.pad(self.image, pw, constant_values=const))