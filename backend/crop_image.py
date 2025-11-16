def crop_image(image_bytes, output_format="PNG"):
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    # Find bounding box of non-transparent pixels
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    
    if bbox and (bbox[0] > 0 or bbox[1] > 0 or bbox[2] < img.width or bbox[3] < img.height):
        cropped = img.crop(bbox)
        buffer = io.BytesIO()
        cropped.save(buffer, format=output_format)
        return buffer.getvalue()
    else:
        return None
