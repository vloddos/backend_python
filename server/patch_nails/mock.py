import io
import base64
from pathlib import Path

import numpy as np
from imageio import imread, imwrite
from skimage.util import img_as_float64, img_as_ubyte

from server.patch_nails.patch_nails import (
    get_r_masks_coordinates,
    get_nails_coordinates,
    Patch,
    input_queue,
    output_queue
)


def patch_nails_mock():
    rng = np.random.default_rng()

    while True:
        patch: Patch = input_queue.get()

        # img_uint8 = patch.img_uint8
        img_float64 = patch.img_float64
        r_masks = np.load(
            Path('/home/vloddos/Desktop/img3.png.uint8.r_masks.npy')
        )

        if not hasattr(patch, 'patch_function') or not hasattr(patch, 'dots'):
            r = inference_model.detect([img_uint8], verbose=0)[0]

        if hasattr(patch, 'patch_function'):
            if hasattr(patch, 'dots'):
                patch.patch_function(img, patch.dots, patch.texture_or_polish)
            else:
                patch.patch_function(
                    img_float64,
                    get_nails_coordinates(
                        get_r_masks_coordinates(
                            # r['masks']
                            r_masks
                        )
                    ),
                    patch.texture_or_polish
                )

            bio = io.BytesIO()
            imwrite(bio, img_as_ubyte(img_float64), format='PNG-PIL')
            output_queue.put(base64.b64encode(bio.getvalue()).decode())
        else:
            output_queue.put(r['masks'].tolist())
