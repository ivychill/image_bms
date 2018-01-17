import cv2
import pytesseract
def recongize_image_high_and_low(img_rgb,pt,w,h):
    image=cv2.imread(img_rgb)
    box1 = (pt[0] + w, pt[1] - 12, pt[0] + w + 40, pt[1] + 8)
    box2 = (pt[0] + w, pt[1] + h - 5, pt[0] + w + 40, pt[1] + h + 15)
    region1 = image.crop(box1)
    region2 = image.crop(box2)
    high = pytesseract.image_to_string(region1, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
    low = pytesseract.image_to_string(region2, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
    print("high: %s, low: %s" % (high, low))
    return high, low