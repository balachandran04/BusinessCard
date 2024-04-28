The Business Card Analyzer is a Python application designed to extract information from business cards using deep learning and analysis techniques. The project aims to simplify the process of digitizing and managing contact information by automatically parsing data from uploaded business card images.

## Features

- **Image Upload**: Users can upload images of business cards through a Streamlit web application interface.
- **Deep Learning**: The application utilizes deep learning algorithms to extract text and relevant information from the uploaded images.
- **Data Analysis**: Extracted text and information are analyzed to identify key details such as name, email, phone number, etc.
- **SQLite Database**: The parsed information is stored in an SQLite3 database for easy retrieval and management.
- **CRUD Operations**: Users can perform Create, Read, Update, and Delete operations on the stored business card data directly from the Streamlit web application.

## Usage

1. Install the required dependencies by running 
2. Run the Streamlit web application using `streamlit run app.py`.
3. Upload an image of a business card through the web interface.
4. The application will automatically extract and analyze the information from the uploaded image.
5. Parsed data will be stored in the SQLite database and displayed on the web application.
6. Users can perform various operations such as updating or deleting entries as needed.

## Dependencies

- Python 3
- google colab
- Streamlit
- SQLite3
- easy OCR
