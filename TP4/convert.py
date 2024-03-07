from PIL import Image, ExifTags

img = Image.open("/home/suri/Bureau/Cours VACANCES/Outil Informatique Collaboratif/TP4/new_img.jpg")
exif_data = img.getexif()
gps_ifd_data = exif_data.get_ifd(ExifTags.IFD.GPSInfo)

# print(gps_ifd_data)
if gps_ifd_data:
    latitude = gps_ifd_data[2]
    longitude = gps_ifd_data[4]
    
    # Convert degrees, minutes, seconds to decimal degrees
    latitude_decimal = float(latitude[0]) + float(latitude[1]/60) + float(latitude[2]/3600)
    longitude_decimal = float(longitude[0]) + float(longitude[1]/60) + float(longitude[2]/3600)
    
    print("Latitude (decimal):", latitude_decimal)
    print("Longitude (decimal):", longitude_decimal)
else:
    print("No GPS information found.")