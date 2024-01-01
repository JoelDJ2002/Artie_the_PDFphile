# Artie: The PDFphile

![Artie Logo](artie_logo.png)

Artie is a PDFphile analyzer designed to streamline the process of analyzing PDF files and providing a chat interface for interacting with multiple PDFs. With Artie, you can quickly extract information from PDF documents and engage in conversations about their contents. This README file provides a comprehensive guide on how to set up Artie and run the application.



## Getting Started

### Prerequisites
Make sure you have the following prerequisites installed:
- Python (>=3.6)
- Pip (Python package installer)

### Installation
1. Clone the Artie repository to your local machine:
   ```bash
   git clone https://github.com/JoelDJ2002/Artie_the_PDFphile   
   ```

2. Install the required dependencies using the provided `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

### API Token Configuration
Create a file named `.env` in the root directory of the Artie project. Place your API token inside the file with the key `HUGGINGFACEHUB_API_TOKEN`:

```env
# .env
HUGGINGFACEHUB_API_TOKEN=<YOUR API TOKEN>
```

Replace `<YOUR API TOKEN>` with your actual API token.

## Running the Application

Once you have installed the required libraries and configured the API token, you can run the Artie application for PDF analysis and chatting. Use the following command:

```bash
streamlit run index.py
```

This will start the Artie application, and you can access it through your web browser.

