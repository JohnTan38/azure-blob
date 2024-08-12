import os
from azure.storage.blob import BlobServiceClient
from flask import Flask, request, redirect, render_template
from dotenv import load_dotenv
from pdf2image import convert_from_path

app = Flask(__name__)
#connect_str = 'AZURE_STORAGE_CONNECTION_STRING'
#connect_str = ''
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
if not connect_str:
    raise ValueError("Please set your environment variable 'AZURE_STORAGE_CONNECTION_STRING'")

container_name = "media"
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)
try:
	container_client = blob_service_client.get_container_client(container=container_name)
	container_client.get_container_properties()
except Exception as e:
	print(e)
	print("Creating container...")
	container_client = blob_service_client.create_container(container_name)


@app.route("/")
def view_media():
                blob_items = container_client.list_blobs()
                images = []
                videos = []
                for blob in blob_items:
                    blob_client = container_client.get_blob_client(blob=blob.name)
                    if blob.name.endswith((".png", ".PNG")) or blob.name.endswith((".jpg", ".JPG")):
                        images.append(blob_client.url)
                    #elif blob.name.endswith(".pdf"):
                        #blob_data = blob_client.download_blob().readall()
                        #with open('temp.pdf', 'wb') as f:
                            #f.write(blob_data)
                        #images_from_path = convert_from_path('temp.pdf', dpi=200,first_page=1,last_page=1)
                        #images_from_path[0].save('temp.png', '.PNG')
                        #with open('temp.png', 'rb') as data:
                            #container_client.upload_blob(name='temp.png',data=data,overwrite=True)
                            #blob_client = container_client.get_blob_client(blob='temp.png')
                            #images.append(blob_client.url)
                    elif blob.name.endswith(".mp4"):
                        videos.append(blob_client.url)
                return render_template('index.html', images=images, videos=videos)
                
   
@app.route("/upload-media", methods=["POST"])
def upload_media():
        for file in request.files.getlist("media"):
            try:
                container_client.upload_blob(file.filename, file)
            except Exception as e:
                print(e)
        return redirect("/")   
    
if __name__ == "__main__":
        app.run(debug=True)