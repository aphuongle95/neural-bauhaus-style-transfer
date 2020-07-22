# to run this file
# install google_images_download library
# install chrome driver and put the path in the argument
# change the keywords for other download
# downloaded image is saved in download/bauhaus painting
from google_images_download import google_images_download   #importing the library

response = google_images_download.googleimagesdownload()   #class instantiation

arguments = {
    "keywords":"bauhaus painting",
    "limit":400,
    "print_urls":True,
    "chromedriver":"/usr/local/bin/chromedriver"
    }   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function
print(paths)
