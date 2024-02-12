import sys
import requests
import json
import re

def retrieve_adobe_token(client_id, client_secret):
    
    url = 'https://pdf-services.adobe.io/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'client_id': client_id, 'client_secret': client_secret}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token = response.json()
            return {"status": "success", "token": token}
        else:
            return {"status": "failure", "code": response.status_code}
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}

client_id = '2a666fad69c8446f92b7190cd3019d46'
client_secret = 'p8e-D8QTvIJSJZ_JBxPTHEgyZ0L1wFYKI-RP'
token_response = retrieve_adobe_token(client_id, client_secret)
print(token_response)



import requests

def upload_asset_to_adobe(client_id, token, media_type):
    url = 'https://pdf-services-ue1.adobe.io/assets'
    headers = {
        'x-api-key': client_id,
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    data = {"mediaType": media_type}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        uploadUri = response_data.get('uploadUri')
        assetID = response_data.get('assetID')
        
        print(f"uploadUri: {uploadUri}, assetID: {assetID}")
        
        return assetID, uploadUri
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None, None

# Example usage
client_id = '2a666fad69c8446f92b7190cd3019d46'
token = 'eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE3MDcyODU0NTExOTRfMzhhNzFmY2ItOTI2Yi00ZmIxLTk2ZjEtOTYzOWIwNGIwOTc0X3VlMSIsIm9yZyI6Ijc3QkEwRUYwNjU5Qjg3RkEwQTQ5NUZGNEBBZG9iZU9yZyIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiIyYTY2NmZhZDY5Yzg0NDZmOTJiNzE5MGNkMzAxOWQ0NiIsInVzZXJfaWQiOiJBRjM0MEVGOTY1OUQwRTVFMEE0OTVGRjNAdGVjaGFjY3QuYWRvYmUuY29tIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJBRjM0MEVGOTY1OUQwRTVFMEE0OTVGRjNAdGVjaGFjY3QuYWRvYmUuY29tIiwiY3RwIjozLCJtb2kiOiJlNWU5ZWYxNCIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsInNjb3BlIjoiRENBUEksb3BlbmlkLEFkb2JlSUQiLCJjcmVhdGVkX2F0IjoiMTcwNzI4NTQ1MTE5NCJ9.UrkH9yfSyfYFuE9ZajsgZdJDQe194jhfDITMm_cFPZVFqNSDbaHJKWefEVCRJ1UAmrH3rhM1ztzv4T3P9e28KMRpQUrI0vmxWNtOcR3MR6C6nPPI7WfjJRRBfXyFgwEULiSdEQizF43P8_BBrpGJ4dPvKDbEHL2LP4f3IDZ4eXslN405I_E4V_hwFN-iArZAatYUJcaA7DO3bIvHjWNT3ApBJAYZSFf1C5f7UXL74Li-LeFUiNFgmMr3HoaphTGNQ5nUVpLJDnynNVtBVTi775ghwE7cWwKNSTnhSfaXBDdbMUHhyY7drFrdQ7zwDXcFG5jxiOBTDX9A8yoTGorvxw'
media_type = 'application/pdf'

assetID, uploadUri = upload_asset_to_adobe(client_id, token, media_type)




import requests

def upload_file_to_uri(uploadUri, file_path):

    if not uploadUri.startswith('http://') and not uploadUri.startswith('https://'):
        return "Invalid URL. Please include the scheme (http:// or https://)."

    headers = {
        'Content-Type': 'application/pdf'
    }


    with open(file_path, 'rb') as file:
        response = requests.put(uploadUri, data=file, headers=headers)
        if response.status_code == 200:
            return 'success'
        else:
            return 'no'

uploadUri = uploadUri  
file_path = '/home/shaik/pdfprocessing/documents_and_codes/modified.pdf'

result = upload_file_to_uri(uploadUri, file_path)
print(result)




target_format = 'docx'
ocr_lang = 'en-US' 
conversion_url = 'https://pdf-services.adobe.io/operation/exportpdf'
conversion_headers = {
        # 'Authorization': f'Bearer {token}','x-api-key': client_id
        'x-api-key': client_id,
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

data={
#'assetID': assetID
        "assetID": assetID,
        "targetFormat": target_format,
        "ocrLang": ocr_lang
}


file_path ='/home/shaik/pdfprocessing/documents_and_codes/modified.pdf'
assetID = assetID
  

conversion_response = requests.post(conversion_url, headers=conversion_headers, json= data)

if conversion_response.status_code == 201:
    print(1)
    location_URI = conversion_response.headers.get('location')
    print(location_URI)
    job_id = location_URI.split('/status')[0].split('/')[-1] if '/status' in location_URI else None
    print(job_id)






import time
import requests
import time
import re

def poll_compress_pdf_status(job_id, token, client_id):
    url = f'https://pdf-services.adobe.io/operation/exportpdf/{job_id}/status'
    headers = {
        'Authorization': f'Bearer {token}',
        'x-api-key': client_id,
    }
    try:
        while True:  
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                status_response = response.json()
                print("Current status:", status_response['status']) 
                
                if status_response['status'] == 'in progress':
                    time.sleep(1)  
                elif status_response['status'] == 'done':
                    print("Response JSON:", status_response)
                    
                    if 'downloadUri' in status_response['asset']:
                        return status_response['asset']['downloadUri']  # 'downloadUri' is inside 'asset'
                    else:
                        print("Error: 'downloadUri' not found in the response.")
                        return None
                elif status_response['status'] == 'failed':
                    print("Job failed")
                    return None
            else:
                print(f"Request failed with status code: {response.status_code}")
                print("Response:")
                print(response.text)
                return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Define job_id, token, and client_id here
job_id = job_id
token = token
client_id = client_id

result = poll_compress_pdf_status(job_id, token, client_id)

if result is not None:
    print("Request successful. Response data:")
    print(result)
else:
    print("Failed to retrieve job status.")





if result is not None:
    try:
        response = requests.get(result, stream=True)  # Add stream=True for efficient downloading
        response.raise_for_status()  # Check for HTTP errors

        # Define the local filename to save the downloaded PDF
        local_filename = "downloaded_file11.docx"

        # Open a local file with write-binary ('wb') mode and write the content
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)

        print(f"File has been downloaded and saved as {local_filename}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")