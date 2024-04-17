import numpy as np
import cv2
import torch

class ImageTransformNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "offsetX": ("FLOAT", {"default": 0, "min": -1000, "max": 1000, "step": 1}),
                "offsetY": ("FLOAT", {"default": 0, "min": -1000, "max": 1000, "step": 1}),
                "zoom": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1})
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("transformed_image", "mask")

    FUNCTION = "transform_image"
    CATEGORY = "Image Processing"

    def transform_image(self, image, offsetX, offsetY, zoom):
        
        
        
        
        
        
        #print("image",image)
        
        if isinstance(image, torch.Tensor):
            # Ensure tensor is on CPU and convert to numpy
            image_np = image.cpu().numpy()
            
            #squeeze the image if it is a 4D tensor
            if len(image_np.shape) == 4:
                image_np = image_np.squeeze(0)
            
            #image_np = np.transpose(image_np, (2,0,1))
            
        else:
            raise ValueError("The input 'image' must be a torch.Tensor.")
        
        
        
        
        print('image shape',image_np.shape)
        
        
        
        
        rows, cols = image_np.shape[0], image_np.shape[1]
        
        #scale offsetX and offsetY by the image size
        offsetX = offsetX * rows
        offsetY = offsetY * cols
        
        print('offsetX',offsetX,'offsetY',offsetY,'zoom',zoom)
        
        
        print('rows',rows,'cols',cols)
        
        M = np.float32([[zoom, 0, offsetX], [0, zoom, offsetY]])

        # Apply affine transformation
        transformed_image_np = cv2.warpAffine(image_np, M, (cols, rows))
        
        # Convert the transformed image back to a tensor
        transformed_image = torch.from_numpy(transformed_image_np).to(image.device)

        # Create mask of the valid area
        mask_np = np.zeros_like(image_np, dtype=np.uint8)
        mask_np = cv2.warpAffine(np.full((rows, cols), 255, dtype=np.uint8), M, (cols, rows), dst=mask_np, borderMode=cv2.BORDER_CONSTANT)
        
        # Convert the mask back to a tensor
        mask = torch.from_numpy(mask_np).to(dtype=torch.uint8, device=image.device).unsqueeze(0)
        
        #just kidding, maybe mask is supposed to be float
        mask = mask.float()
        
        #unsqueeze image
        transformed_image = transformed_image.unsqueeze(0)
        
        #our image appeasr to be wierd, maybe we need to divide by 255
        transformed_image = transformed_image
        
        
        print('transformed_image',transformed_image.shape)
        #print('mask',mask.shape, mask.dtype)
        
        #print("image",transformed_image)
        
        #divide mask by 255?
        mask = mask / 255.0
        
        #invert mask?
        mask = 1 - mask
        
        #print("mask",mask)

        return transformed_image, mask

# Example of how you might set up the node mappings and display names for UI integration.
NODE_CLASS_MAPPINGS = {
    "ImageTransformNode": ImageTransformNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageTransformNode": "Image Transformation Node"
}
