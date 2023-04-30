import requests

s = open("Image.png","wb")
request = requests.get(input("Enter the url which you want to download an image (note:include https://) : "))
s.write(request.content)
s.close()
print("Downloaded")
