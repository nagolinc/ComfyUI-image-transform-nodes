this adds 2 comfyui nodes

ImageTransformNode, which accepts an offsetX an offsetY and a zoom factor, and applies these transformations to the image it receives. This is useful for creating parallax effects, or for zooming in on a specific part of the image.

JsonParserNode which accepts a json string formatted like:
{
    'offsetX': 0,
    'offsetY': 0,
    'zoom': 0.5
}

and returns the 3 values as separate outputs. This is useful for creating a UI that allows the user to control the ImageTransformNode.