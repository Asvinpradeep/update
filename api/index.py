from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from google.auth.transport.requests import Request
import google.auth

app = Flask(__name__)

# Firebase credentials (this should be stored securely, not directly in the code)
service_account_info = {
  "type": "service_account",
  "project_id": "lumethrv",
  "private_key_id": "4da8484822f4aab75eb8df8aa36eeed620423773",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCMjHPmoIJLpnGu\nN5VOSHUF7ahF2HObJtf/pVlKoMNScFSQrDv4u0Rs45RXI2w2r4eW41KCpL0neJAz\no8A+uZ6T2HkCUvDZEzXGCQz8CJDPkKf6kPhQJi27sQcJbhKjFY3fu2krXqOKs9P8\nXPCJDSikv9kRuzjiGGT9BYtdk0imQo5FvMGcXeionbz4WtNH61cEDRrHpTck//cu\n6xF7RdX2+9ASWvL94OvMON0+5ZuDIzg3/TQF/pSjDf3K1PFguRUERAuPGo089XpX\nV7E4K1LEAVQnXgI1C/7ty9O4dfv+zZ1KL8wp91Bodu80d9ZaspmntZ62BZeOg2/6\npDY/fXkdAgMBAAECggEAPzacmknu0F+YGadeO8tS9suhN2jW9h1OYOjZdDtCHj3v\nivIsNv7jE6Z3/YktDpt7/F1ZqvC1Mp+DG/a2bH/H1u8x3d23/aoqMVu4v1KK7xA8\nvPGe/U1unFBOvesH7tmu6cW804jJPYUL/yE9/iYw9Yhj9Rmjx+z43uQzfm7T6hKy\nfU+qnkVQWDNR1eX3HYF3otaPzRjbGxhgcoBp1gHSeS5N13TjLD+KZpoxb9q0UBkK\nesOY8kcfVj7NyeB4Zj1ITRhyQC38esxuOtoXwZxQoFfansN6BKU7JW4Ft4s1HmH3\n0eQ8mPEUQLeuB/rMylnQ8OGiA9Pb+ILaPnt8vFPxcQKBgQDDkh/KLgviD+eZ3No1\ncepBym/S0sjfc3tzo7uuTIrqPQK0Yd5h37eld+IO4fALA61oWS2pVxAkRUj0lga7\nmqUJVorJG/+qq67+oKfJELLgyhLVEQCvLqcoDTwsFewIzfpVpwL+O/xb7tnBRIEG\nRsNHH56G6irac1cM3E6zTFrXMwKBgQC3+gM9+Kf8IGjJteOm33u0pRTMhxxmzkl1\nqEo0MV+Vt/OO6DiF2ia3N1xUVof1OEz4Tz8YRI55ATQQq2OA273VUwuiU7KorwFF\noSU8gXtGRHrSINZ9uDNNP5mZELEYqVjEWw3UT8JaWiy8jG0qbUxunOl0OiNY6ZMf\n4n8aLNUubwKBgQCLktnFPR+V8qvjj07cHbSFx6gO2ggqEQzl9tCXEGGD0o7/lWlU\niIlUOj7HSFA8TB+R/TMtS8llWV070WZ0tWVbSLw70xOgBm8ZoiacxKIk85KFJWFL\npQv+9ZMgE3Ukw3wJbOwh7UWphsk5uV4r0IzFUbedqblztiVGNGSmabPbKQKBgQCz\nfZ0aIfWqOuhhGy7eiJ0FUiWnoY3pEwuCWc0DfMQXqt9ZpmA23u30xHM06TM94E7f\n11jkUUZ68dydAslSV5CuhpYMKgJdJlhkWWKd1Gmz1W3KgjUhdMvAavNs7WcKe3Xa\nJEeqwqIISn/o+EwtH3N5W2c8eNgxj7h1XCHLJMBbywKBgErhOp/ffblcYV4Dh240\nqyt7nbxxH6UJV8pclis4g5bBQkcSQkjsskcP8DIqXm9BqPJ6cIqggrfR3sM5nDrl\nm6Q7HF0fqaozTZNPvx9nFV719w32fgoq6T4YE2o/31vGQKl9mA4YOLNDmRqCniDr\ngeSaO/0HWTwLtEq8PghLmjj7\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-mmudl@lumethrv.iam.gserviceaccount.com",
  "client_id": "118272570511746214100",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mmudl%40lumethrv.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Function to authenticate using JWT token
def authenticate_via_jwt():
    credentials, project = google.auth.load_credentials_from_dict(service_account_info)
    credentials.refresh(Request())  # Refresh the credentials
    return credentials

# Authenticate Firebase Admin SDK using JWT credentials
credentials = authenticate_via_jwt()
firebase_admin.initialize_app(credentials)

# Initialize Firestore client
db = firestore.client()

@app.route('/update_documents', methods=['POST'])
def update_documents():
    try:
        data = request.get_json()

        # Extract document references and fields to update
        shop_refs = data.get('shopRefs', [])
        service_refs = data.get('serviceRefs', [])
        service_offer_refs = data.get('serviceOfferRefs', [])
        offer_refs = data.get('offerRefs', [])
        update_fields = data.get('updateFields', {})

        if not update_fields or not isinstance(update_fields, dict):
            return jsonify({'error': 'updateFields must be a dictionary with fields to update'}), 400

        all_refs = shop_refs + service_refs + service_offer_refs + offer_refs
        updated_docs = []

        # Iterate over each document reference
        for ref_path in all_refs:
            doc_ref = db.document(ref_path)
            # Use set() with merge=True to update or create fields
            doc_ref.set(update_fields, merge=True)
            updated_docs.append(ref_path)

        return jsonify({'message': 'Documents updated successfully', 'updatedDocs': updated_docs}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
