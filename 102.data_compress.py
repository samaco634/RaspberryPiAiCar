import sys
import os 
import glob
import zipfile

def main():

#    condition =  "./data/*/*.png"
    condition =  "./data/*.png"
    png_files = glob.glob(condition)
    print(png_files)

    with zipfile.ZipFile("car_image.zip", 'w') as my_zip:
    #my_zip = zipfile.ZipFile("car_image_angle.zip", 'w')
        for file in png_files:
            my_zip.write(file)
    my_zip.close()

if __name__ =='__main__':
	main()
