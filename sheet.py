import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import pygsheets

# Initialize Firebase
cred = credentials.Certificate(r"beform-ff5fc-firebase-adminsdk-ux5xr-3ed1e62e71.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to fetch data from Firestore collection and convert it into DataFrame
def fetch_firestore_data():
    data_list = []
    collection_ref = db.collection('dd_product')
    docs = collection_ref.stream()
    for doc in docs:
        data_list.append(doc.to_dict())
    df = pd.DataFrame(data_list)
    return df

# Function to update Google Sheets with DataFrame data
def update_google_sheet(df):
    # Initialize Google Sheets
    gc = pygsheets.authorize(service_account_file='project-12-feb-2024-b51713fec6eb.json')
    sh = gc.open('Beform Sales Data')
    worksheet = sh.sheet1  # Assuming you're using the first sheet
    
    # Convert DataFrame to list of lists for updating Google Sheet
    values = df.astype(str).values.tolist()  # Convert all values to strings
    
    # Update Google Sheet starting from the second row (index 1) since the first row contains headings
    worksheet.append_table(crange='A2', values=values)


# Example usage
df = fetch_firestore_data()
update_google_sheet(df)

