import boto3
import os
import customtkinter as ctk
from tkinter import messagebox
from botocore import UNSIGNED
from botocore.config import Config

# Configuration
bucket_name = 'umbra-open-data-catalog'
prefix = 'sar-data/tasks/'  # Higher-level prefix for exploration
local_download_path = r'path\to\umbra_data'  # Update this path

# Create a boto3 client with no AWS credentials
s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

def download_file(bucket, key, download_path):
    local_filename = os.path.join(download_path, key.replace('/', '\\'))
    if not os.path.exists(os.path.dirname(local_filename)):
        os.makedirs(os.path.dirname(local_filename))
    s3_client.download_file(bucket, key, local_filename)

def main(selected_file_types):
    paginator = s3_client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_name, 'Prefix': prefix}
    
    for page in paginator.paginate(**operation_parameters):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if any(key.endswith(ext) for ext in selected_file_types):
                    print(f'Downloading {key}')
                    download_file(bucket, key, local_download_path)
        else:
            print('No contents found in this page')

def start_download():
    selected_file_types = []
    if var_cphd.get():
        selected_file_types.append('.cphd')
    if var_nitf.get():
        selected_file_types.append('.nitf')
    if var_tif.get():
        selected_file_types.append('.tif')
    if var_json.get():
        selected_file_types.append('.json')
    
    if not selected_file_types:
        messagebox.showwarning("No Selection", "Please select at least one file type.")
        return

    main(selected_file_types)
    messagebox.showinfo("Download Complete", "Selected files have been downloaded.")

# GUI setup
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = ctk.CTk()
root.title("S3 File Downloader")
root.geometry("400x300")
root.configure(bg='#1B4D3E')

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Select file types to download:", font=("Arial", 14))
label.pack(pady=10)

var_cphd = ctk.BooleanVar()
check_cphd = ctk.CTkCheckBox(frame, text=".cphd", variable=var_cphd, font=("Arial", 12))
check_cphd.pack(pady=5)

var_nitf = ctk.BooleanVar()
check_nitf = ctk.CTkCheckBox(frame, text=".nitf", variable=var_nitf, font=("Arial", 12))
check_nitf.pack(pady=5)

var_tif = ctk.BooleanVar()
check_tif = ctk.CTkCheckBox(frame, text=".tif", variable=var_tif, font=("Arial", 12))
check_tif.pack(pady=5)

var_json = ctk.BooleanVar()
check_json = ctk.CTkCheckBox(frame, text=".json", variable=var_json, font=("Arial", 12))
check_json.pack(pady=5)

download_button = ctk.CTkButton(frame, text="Start Download", command=start_download, font=("Arial", 12))
download_button.pack(pady=20)

root.mainloop()
