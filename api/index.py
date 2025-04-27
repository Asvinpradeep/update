from flask import Flask, request, jsonify
from google.cloud import firestore
from google.oauth2 import service_account

# Paste your service account JSON here (or load from a secure location)
service_account_info = {
  "type": "service_account",
  "project_id": "lumethrv",
  "private_key_id": "68dcf4f342038ec3591d999c7cc95c80b06266de",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDBW9oibSBPRBE4\nr5NlkxcOKJG/9tcrXZ6bo4R+f5WbmJUoC+Q8Im9Jl8Wra1fS/DGIqrVqy+hcO5O/\nSB+BkQtgPqUH4V5KZe2XhjBO4heaOEMZaO45IDpl6rS1KRb+NKg1uD2y7TdFSApq\nH/CzXYkaGC4vhOjxqHQHaFBPJdj29ogh0SYr7LZBL1+FVtS9YJGdZDWsNfvJHm+P\ni3+gYo0rh2cad71kDfmv3ewpZ7CpdeUOep+SR+RKKjJvABCymoOZcQLzO9gpDOW8\nBLDZdpJ99jWmVBv7LReIHEVwD8bkzd/u2sztT5BHXunjree2UpmcZeVULIdsmEqx\nF6K1DzjXAgMBAAECggEAAqcC6AP9NHknj1KBQBxzbYNK9IorS3H+Uf49PAr9/2Np\ncGIxYE3MnwLQ+FgBnWhOOaS11mAzsMg0b6RKolleAZT6aJBD3dtmFfUGRp69WiU5\nbmjNE8WIZ4t/rRiCMzx/rjT3y7OLVYz2b5w+jgdTcSMxxv8Yvu/jn5Jjv6IyRrj2\n357n0ch72Rtn43u7A60nK9WWzhH2KLXw1SuiEpc8pqZlzPAzPdCoDe+04UFbFH5E\napbJCWwP3Km9cRS1oO69BY5VAuR8pXEovB5TloMD3ou3Pu9uHQlZapYp1oOx9Ate\nBClvGzUJuv70LSsDkAeJcScSeDqFtBTbbYTpzvFQ+QKBgQDDtydQ2gDM0CvyAyzx\nIYP3T4umh5a+TTwPPVk9F4wDUGvQbsnhfnjRUJRiVRkrd+DHMXZqmByvxHFHk6Hj\nhXAxGnuj3LmmrHtLAya8v+/obp9knd7vvftmI0cLB2A9IjdNP9bCsNvfDzMi2tUU\nskAOuaPZ3jR9x8dewdwXUPZjqwKBgQD86t5jgRsAn6RRoipRIDpVHF2lKqsihmRb\ncs+p1sY9AK6ufq/NFbx96pp2efhtUReQF+eNepFaeU5jE7Ucejsi22evCrEGggje\naopRQzbSnvoLOT58H7tjYz54Ak4ESAy7QPhJ1wk1n6EMxCpXs73VlN8yrBNk4U9+\nw5EqCzdThQKBgAyEBuiduFVgrp7AYzxcV1MWbCjPHO24hLG4y58jhVmk5/AhVZms\n+87u5z5OkNh9xwsV96ujZJo85r2cDEs/ekg5mFSHRfwJpazLW8vQPmhPwrOtgNc2\nAACtGtryss3WBVFUVsiGhNkD4NJGyj+TkpMefgLtuc+dWfuOTCPVkpwXAoGAD3K9\nILDLGG+n1sCj+w6P4ZD4+1Su3U3+JUPPAV24ABPhl5DvZgR03fANfT0X+n1ghhGf\nuBmLdU5BhnW2s0WYBRoHrD5n77DTn9o8FpiXaagCN9tIQMajaH+wWh4x67sG5A0k\n3UXAL0FP0frNZ0v4RWpxc6PlD11fwKtrW3kR6Q0CgYB/4fX1eSXWo2WCa22518iO\nxSdMJLbCyTilqxAiWc/6W/n06/OJfPMLQEq/R/xcqhm5SSP3xalP9MFn/QChSBxF\nwdwLwphGKJ2TuHXPx2H2lRkGMds+1wNr/HUhpQ2YBvozvHrBKxwaJ0epnoEtr4Ya\nPYWTWa6y++jxUZAW3PHmLA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-mmudl@lumethrv.iam.gserviceaccount.com",
  "client_id": "118272570511746214100",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mmudl%40lumethrv.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firestore client
creds = service_account.Credentials.from_service_account_info(service_account_info)
db = firestore.Client(credentials=creds)

# Create Flask app\ napp = Flask(__name__)

# Helper function to perform reference updates
 def perform_update(document_id):
    add_doc_ref = db.collection('adds').document(document_id)
    add_doc = add_doc_ref.get()
    if not add_doc.exists:
        return None, f"Document '{document_id}' not found.", 404

    add_data = add_doc.to_dict()
    # Gather fields to update
    fields_to_update = {
        'start': add_data.get('start'),
        'end': add_data.get('end'),
        'indexlist': add_data.get('indexlist', [])
    }

    # Update each reference list
    for key in ['shopref', 'serviceref', 'serviceoffer', 'offerref']:
        for ref in add_data.get(key, []):
            ref.update(fields_to_update)

    return True, f"All referenced documents for '{document_id}' updated successfully!", 200

# Define API endpoint
@app.route('/update_references', methods=['POST'])
def update_references_route():
    data = request.get_json()
    if not data or 'document_id' not in data:
        return jsonify({'status': 'error', 'message': "Missing 'document_id' in request."}), 400

    document_id = data['document_id']
    success, message, status_code = perform_update(document_id)
    status = 'success' if success else 'error'
    return jsonify({'status': status, 'message': message}), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
