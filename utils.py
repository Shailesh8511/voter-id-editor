import cv2
from PIL import Image
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas

def process_voter_id(sd_pdf_path, ssd_img_path, output_pdf_path):
    images = convert_from_path(sd_pdf_path)
    sd_img_path = sd_pdf_path.replace(".pdf", ".jpg")
    images[0].save(sd_img_path, 'JPEG')

    sd_img = cv2.imread(sd_img_path)
    ssd_img = cv2.imread(ssd_img_path)

    # Remove text from SD using inpainting (hardcoded region)
    mask = cv2.rectangle(sd_img.copy(), (190, 720), (1000, 760), (255, 255, 255), -1)
    inpainted = cv2.inpaint(sd_img, cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY), 3, cv2.INPAINT_TELEA)

    # Crop hologram from SSD
    hologram = ssd_img[360:450, 615:745]  # y1:y2, x1:x2

    # Paste on SD
    inpainted[720:810, 870:1000] = hologram

    # Save edited image
    result_img_path = sd_img_path.replace(".jpg", "_edited.jpg")
    cv2.imwrite(result_img_path, inpainted)

    # Convert to PDF
    image = Image.open(result_img_path)
    image.save(output_pdf_path, "PDF", resolution=100.0)
