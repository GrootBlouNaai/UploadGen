# Copyright (C) 2024 officialputuid

import os
import sys
import argparse
import requests
import base64

def upload_pixeldrain(api_key, file_path):
    print(f"[⌛] Uploading {file_path} to Pixeldrain.com . . .")

    # Validate API key using adapted method
    try:
        # Encode API key to Base64
        encoded_api_key = base64.b64encode(f":{api_key}".encode()).decode()

        # Use Authorization header with encoded key
        check_api_response = requests.get(
            "https://pixeldrain.com/api/user/files",
            headers={
                "Authorization": f"Basic {encoded_api_key}"
            }
        )
        if check_api_response.status_code == 200:
            print("[✔️] Pixeldrain API key is valid!")
        else:
            print(f"[❌] Pixeldrain API key is invalid! Status code: {check_api_response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"[❌] Failed to check API key: {e}\n")
        return

    # Continue with file upload
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://pixeldrain.com/api/file",
                auth=('', api_key),
                files={'file': f},
            )
        response.raise_for_status()
        response_json = response.json()
        file_id = response_json.get('id')
        if file_id:
            print("[✔️] File uploaded successfully!")
            print(f"[🔗] Your file URL: https://pixeldrain.com/u/{file_id}\n")
        else:
            print("[❌] Upload failed.")
    except requests.exceptions.SSLError as ssl_err:
        print(f"[❌] Failed to upload file: SSL issue. Error message: {ssl_err}\n")
    except requests.exceptions.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
    except requests.exceptions.JSONDecodeError:
        print("[❌] Unable to decode response as JSON.\n")
    except Exception as e:
        print(f"[❌] An unknown error occurred: {e}\n")
        sys.exit(1)

def upload_gofile(file_path):
    print(f"[⌛] Uploading {file_path} to Gofile.io . . .")
    try:
        server_response = requests.get("https://api.gofile.io/servers")
        server_response.raise_for_status()
        server = server_response.json()['data']['servers'][0]['name']
    except requests.RequestException as e:
        print(f"[❌] Failed to retrieve server information: {e}\n")
        sys.exit(1)

    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                f"https://{server}.gofile.io/uploadFile",
                files={'file': f}
            )
            upload_response.raise_for_status()
        link = upload_response.json()['data']['downloadPage']
        print("[✔️] File uploaded successfully!")
        print(f"[🔗] Your file URL: {link}\n")
    except requests.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
        sys.exit(1)

def upload_bashupload(file_path):
    print(f"[⌛] Uploading {file_path} to Bashupload.com . . .")
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://bashupload.com",
                files={'file': f}
            )
        response.raise_for_status()
        # Extract URL from response
        response_text = response.text
        url_start = response_text.find("https://bashupload.com/")
        if url_start != -1:
            url_end = response_text.find("\n", url_start)
            if url_end == -1:
                url_end = len(response_text)
            link = response_text[url_start:url_end].strip()
            print("[✔️] File uploaded successfully!")
            print(f"[🔗] Your file URL: {link}\n")
        else:
            print("[❌] Failed to upload file. URL not found.\n")
    except requests.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
        sys.exit(1)

def upload_devuploads(api_key, file_path):
    print(f"[⌛] Uploading {file_path} to Devuploads.com . . .")
    url = "https://devuploads.com/api/upload/server"

    try:
        # Validate API key
        check_response = requests.get(f"{url}?key={api_key}")
        check_response.raise_for_status()
        res_json = check_response.json()

        res_status = res_json.get("status")
        sess_id = res_json.get("sess_id")
        server_url = res_json.get("result")

        if res_status == 200:
            print("[✔️] Devuploads API key is valid!")
            if not sess_id or not server_url:
                print(f"[❌] Server information not available. API key valid but server information empty.")
                return
        else:
            print(f"[❌] Devuploads API key is invalid! Status code: {res_status}")
            return

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"[❌] File {file_path} is empty.\n[❌] Devuploads cannot upload files with 0 bytes")
            return

        # Continue with file upload
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                server_url,
                files={"file": f},
                data={"sess_id": sess_id, "utype": "reg"},
            )
        upload_response.raise_for_status()

        upload_response_json = upload_response.json()

        if isinstance(upload_response_json, list):
            upload_response_json = upload_response_json[0]

        file_code = upload_response_json.get("file_code")
        file_status = upload_response_json.get("file_status")

        if file_code == 'undef':
            print(f"[❌] Upload failed: {file_status}\n")
        elif file_code:
            print("[✔️] File uploaded successfully!")
            print(f"[🔗] Your file URL: https://devuploads.com/{file_code}\n")
        else:
            print(f"[❌] Upload failed: {upload_response_json}\n")

    except requests.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
        sys.exit(1)

def upload_fileio(file_path):
    print(f"[⌛] Uploading {file_path} to File.io . . .")
    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                'https://file.io',
                files={'file': f}
            )
            upload_response.raise_for_status()
        link = upload_response.json()['link']
        print("[✔️] File uploaded successfully!")
        print(f"[🔗] Your file URL: {link}\n")
    except requests.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
        sys.exit(1)

def upload_uguu(file_path):
    print(f"[⌛] Uploading {file_path} to Uguu.se . . .")
    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                'https://uguu.se/upload',
                files={'files[]': f}
            )
            upload_response.raise_for_status()

        # Process response to get download link
        response_json = upload_response.json()
        if response_json.get('success'):
            file_url = response_json['files'][0]['url']
            print("[✔️] File uploaded successfully!")
            print(f"[🔗] Your file URL: {file_url}\n")
        else:
            print(f"[❌] Failed to upload file: {response_json}\n")
            sys.exit(1)
    except requests.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
        sys.exit(1)

def upload_0x0st(file_path):
    print(f"[⌛] Uploading {file_path} to 0x0.st . . .")
    
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://0x0.st',
                files={'file': f}
            )
            response.raise_for_status()
        
        # Response from 0x0.st is in plain text
        link = response.text.strip()
        print("[✔️] File uploaded successfully!")
        print(f"[🔗] Your file URL: {link}\n")
    
    except requests.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
        sys.exit(1)

# ASCII art
pixeldrain_art = "\033[92m" + r"""
 ____  _          _     _           _                            
|  _ \(_)_  _____| | __| |_ __ __ _(_)_ __    ___ ___  _ __ ___  
| |_) | \ \/ / _ \ |/ _` | '__/ _` | | '_ \  / __/ _ \| '_ ` _ \ 
|  __/| |>  <  __/ | (_| | | | (_| | | | | || (_| (_) | | | | | |
|_|   |_/_/\_\___|_|\__,_|_|  \__,_|_|_| |_(_)___\___/|_| |_| |_|
""" + "\033[0m"

gofile_art = "\033[92m" + r"""
  ____        __ _ _        _       
 / ___| ___  / _(_) | ___  (_) ___  
| |  _ / _ \| |_| | |/ _ \ | |/ _ \ 
| |_| | (_) |  _| | |  __/_| | (_) |
 \____|\___/|_| |_|_|\___(_)_|\___/ 
""" + "\033[0m"

bashupload_art = "\033[92m" + r"""
 ____            _                 _                 _                      
| __ )  __ _ ___| |__  _   _ _ __ | | ___   __ _  __| |  ___ ___  _ __ ___  
|  _ \ / _` / __| '_ \| | | | '_ \| |/ _ \ / _` |/ _` | / __/ _ \| '_ ` _ \ 
| |_) | (_| \__ \ | | | |_| | |_) | | (_) | (_| | (_| || (_| (_) | | | | | |
|____/ \__,_|___/_| |_|\__,_| .__/|_|\___/ \__,_|\__,_(_)___\___/|_| |_| |_|
                            |_|                                              
""" + "\033[0m"

devuploads_art = "\033[92m" + r"""
 ____                         _                 _                          
|  _ \  _____   ___   _ _ __ | | ___   __ _  __| |___   ___ ___  _ __ ___  
| | | |/ _ \ \ / / | | | '_ \| |/ _ \ / _` |/ _` / __| / __/ _ \| '_ ` _ \ 
| |_| |  __/\ V /| |_| | |_) | | (_) | (_| | (_| \__ \| (_| (_) | | | | | |
|____/ \___| \_/  \__,_| .__/|_|\___/ \__,_|\__,_|___(_)___\___/|_| |_| |_|
                       |_|                                                 
""" + "\033[0m"

file_art = "\033[92m" + r"""
 _____ _ _        _       
|  ___(_) | ___  (_) ___  
| |_  | | |/ _ \ | |/ _ \ 
|  _| | | |  __/_| | (_) |
|_|   |_|_|\___(_)_|\___/ 
""" + "\033[0m"

uguu_art = "\033[92m" + r"""
 _   _                              
| | | | __ _ _   _ _   _   ___  ___ 
| | | |/ _` | | | | | | | / __|/ _ \
| |_| | (_| | |_| | |_| |_\__ \  __/
 \___/ \__, |\__,_|\__,_(_)___/\___|
       |___/                      
""" + "\033[0m"

oxost_art = "\033[92m" + r"""
  ___        ___       _   
 / _ \__  __/ _ \  ___| |_ 
| | | \ \/ / | | |/ __| __|
| |_| |>  <| |_| |\__ \ |_ 
 \___//_/\_\\___(_)___/\__|
""" + "\033[0m"

def print_ascii_art(service):
    if service == 1:
        print(pixeldrain_art)
    elif service == 2:
        print(gofile_art)
    elif service == 3:
        print(bashupload_art)
    elif service == 4:
        print(devuploads_art)
    elif service == 5:
        print(file_art)
    elif service == 6:
        print(uguu_art)
    elif service == 7:
        print(oxost_art)

def interactive_mode():
    print("\033[92m" + r"""
 _   _       _                 _  ____            
| | | |_ __ | | ___   __ _  __| |/ ___| ___ _ __  
| | | | '_ \| |/ _ \ / _` |/ _` | |  _ / _ \ '_ \ 
| |_| | |_) | | (_) | (_| | (_| | |_| |  __/ | | |
 \___/| .__/|_|\___/ \__,_|\__,_|\____|\___|_| |_|
      |_|                                         

Version: v1.7
by officialputuid   
    """ + "\033[0m")

    while True:
        print("Choose the service to upload to:")
        print("1. Pixeldrain.com (Requires API)")
        print("2. GoFile.io")
        print("3. Bashupload.com (Temporary)")
        print("4. Devuploads.com (Requires API)")
        print("5. File.io")
        print("6. Uguu.se")
        print("7. 0x0.st")

        try:
            choice = input("\n[❓] Enter your choice number: ")

            # ASCII art
            print_ascii_art(int(choice))

            if choice == '1':
                while True:
                    print("\n[🛈] You chose:\n[1] Pixeldrain.com (Requires API)\n")
                    api_key = input("[🔑] Enter your Pixeldrain API key: ").strip()
                    if api_key:
                        break
                    print("[❌] API key cannot be empty. Please enter a valid API key.")
                upload_pixeldrain(api_key, get_file_path())
            elif choice == '2':
                print("[🛈] You chose:\n[2] GoFile.io\n")
                upload_gofile(get_file_path())
            elif choice == '3':
                print("[🛈] You chose:\n[3] Bashupload.com\n[🛈] File stored for 3 days and can only be downloaded once.\n")
                upload_bashupload(get_file_path())
            elif choice == '4':
                while True:
                    print("\n[🛈] You chose:\n[4] Devuploads.com (Requires API)\n[🛈] Devuploads cannot upload files with 0 bytes\n")
                    api_key = input("[🔑] Enter your Devuploads API key: ").strip()
                    if api_key:
                        break
                    print("[❌] API key cannot be empty. Please enter a valid API key.")
                upload_devuploads(api_key, get_file_path())
            elif choice == '5':
                print("[🛈] You chose:\n[5] File.io\n")
                upload_fileio(get_file_path())
            elif choice == '6':
                print("[🛈] You chose:\n[6] Uguu.se\n")
                upload_uguu(get_file_path())
            elif choice == '7':
                print("[🛈] You chose:\n[7] 0x0.st\n")
                upload_0x0st(get_file_path())
            else:
                print("[❌] Invalid choice.")
                sys.exit(1)

            # Ask user if they want to upload another file
            repeat = input("[🔄] Do you want to upload another file? (y/n): ").strip().lower()
            if repeat == 'n':
                print("[✔️] Thank you for using UploadGen!\n")
                break

        except KeyboardInterrupt:
            print("\n[✔️] Program closed!\n")
            sys.exit(0)

def get_file_path():
    while True:
        file_path = input("[📁] Type the file to upload: ").strip()
        if file_path and os.path.isfile(os.path.abspath(file_path)):
            return os.path.abspath(file_path)
        print("[❌] File not found! Please enter a valid file.")

def main():
    parser = argparse.ArgumentParser(description="Upload file to various file sharing services.")
    parser.add_argument("-s", "--service", type=int, choices=[1, 2, 3, 4, 5, 6, 7],
                        help="Choose service: 1=Pixeldrain, 2=GoFile, 3=Bashupload, 4=Devuploads, 5=File, 6=Uguu, 7=0x0st")
    parser.add_argument("-f", "--file", help="Path of the file to upload")

    args = parser.parse_args()

    if args.service and args.file:
        if not os.path.isfile(os.path.abspath(args.file)):
            print("\n[❌] File not found!\n")
            sys.exit(1)

        file_path = os.path.abspath(args.file)

        # ASCII art
        print_ascii_art(args.service)

        if args.service == 1:
            print("\n[🛈] You chose: [1] Pixeldrain.com (Requires API)\n")
            api_key = input("[🔑] Enter your Pixeldrain API key: ").strip()
            upload_pixeldrain(api_key, file_path)
        elif args.service == 2:
            print("\n[🛈] You chose: [2] GoFile.io\n")
            upload_gofile(file_path)
        elif args.service == 3:
            print("\n[🛈] You chose: [3] Bashupload.com\n[🛈] File stored for 3 days and can only be downloaded once.\n")
            upload_bashupload(file_path)
        elif args.service == 4:
            print("\n[🛈] You chose: [4] Devuploads.com (Requires API)\n[🛈] Devuploads cannot upload files with 0 bytes\n")
            api_key = input("[🔑] Enter your Devuploads API key: ").strip()
            upload_devuploads(api_key, file_path)
        elif args.service == 5:
            print("\n[🛈] You chose: [5] File.io\n")
            upload_fileio(file_path)
        elif args.service == 6:
            print("\n[🛈] You chose: [6] Uguu.se\n")
            upload_uguu(file_path)
        elif args.service == 7:
            print("\n[🛈] You chose: [7] 0x0.st\n")
            upload_0x0st(file_path)
    else:
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[✔️] Program closed!\n")
        sys.exit(0)
