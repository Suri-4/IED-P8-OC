from PIL import ExifTags, Image

image = Image.open("/home/suri/Bureau/Cours VACANCES/Outil Informatique Collaboratif/TP4/IMG_3197_with_gps (copie) test.jpg")
exif = image.getexif()
gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)

new_gps_info = {
    1: 'N',
    2: (49.0, 9.0, 50.0),
    3: 'E',
    4: (5.0, 23.0, 32.0)
}
print(gps_ifd)

exif[ExifTags.IFD.GPSInfo] = new_gps_info

image.save("/home/suri/Bureau/Cours VACANCES/Outil Informatique Collaboratif/TP4/IMG_3197_with_gps (copie) test.jpg", exif=exif)