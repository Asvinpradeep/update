from flask import Flask, request, jsonify
from google.cloud import firestore
from google.oauth2 import service_account

# Initialize Flask app
app = Flask(__name__)

# Service Account JSON for Firestore
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

def perform_update(document_id):
    try:
        print(f"🔎 Fetching document ID: {document_id}")

        # Fetch the 'adds' document
        add_doc_ref = db.collection('adds').document(document_id)
        add_doc = add_doc_ref.get()

        if not add_doc.exists:
            print(f"❌ Document {document_id} not found.")
            return

        print(f"✅ Document {document_id} fetched successfully.")

        add_data = add_doc.to_dict()

        # Fields to update
        start = add_data.get('start')
        end = add_data.get('end')
        indexlist = add_data.get('indexlist', [])

        print(f"📝 Fields to update - start: {start}, end: {end}, indexlist: {indexlist}")

        fields_to_update = {
            'start': start,
            'end': end,
            'indexlist': indexlist
        }

        # Helper function to update reference documents
        def update_documents(ref_list, ref_name):
            print(f"🔧 Updating {len(ref_list)} documents in {ref_name}...")
            for ref in ref_list:
                ref.update(fields_to_update)
                print(f"  ➔ Updated {ref.id}")

        # Update all references
        shop_refs = add_data.get('shopref', [])
        service_refs = add_data.get('serviceref', [])
        serviceoffer_refs = add_data.get('serviceoffer', [])
        offer_refs = add_data.get('offerref', [])

        # Check if references exist before updating
        if shop_refs:
            update_documents(shop_refs, "shopref")
        if service_refs:
            update_documents(service_refs, "serviceref")
        if serviceoffer_refs:
            update_documents(serviceoffer_refs, "serviceoffer")
        if offer_refs:
            update_documents(offer_refs, "offerref")

        print(f"🎉 All referenced documents for {document_id} updated successfully!")

    except Exception as e:
        print("❗ Error:", str(e))
        return jsonify({"error": str(e)}), 500

# API endpoint to update references
@app.route('/update_references', methods=['POST'])
def update_references():
    try:
        # Get the document_id from the request payload
        data = request.get_json()
        document_id = data.get('document_id')

        if not document_id:
            return jsonify({"error": "document_id is required"}), 400

        # Call the function to perform the update
        perform_update(document_id)

        return jsonify({"message": f"References for document {document_id} updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
