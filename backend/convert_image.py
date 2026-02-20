def convert_image(image_bytes):
    from PIL import Image
    import io

    buffer = io.BytesIO()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    img.save(buffer, format="WEBP")
    return buffer.getvalue()
