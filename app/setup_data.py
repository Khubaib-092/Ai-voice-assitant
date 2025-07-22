import os
import requests
from django.conf import settings

def setup_sample_pdf():
    data_dir = os.path.join(settings.BASE_DIR, 'app', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}")
    else:
        print(f"Directory already exists: {data_dir}")

    pdf_path = os.path.join(data_dir, 'sample_company_profile.pdf')

    if not os.path.exists(pdf_path):
        url = "https://arxiv.org/pdf/1706.03762.pdf"  # Example sample PDF (Transformer paper)
        response = requests.get(url)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded sample PDF to: {pdf_path}")
        else:
            print("Failed to download PDF")
    else:
        print("Sample PDF already exists.")

if __name__ == "__main__":
    setup_sample_pdf()
