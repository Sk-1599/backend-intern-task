from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
contacts = []

def find_contact(email, phone):
    for contact in contacts:
        if contact["emails"] == email or contact["phoneNumbers"] == phone:
            return handle_bad_request()
    return None

def create_contact(email, phone, link_precedence="primary"):
    contact_id = len(contacts) + 1
    new_contact = {
        "contactId": contact_id,
        "emails": [email],
        "phoneNumbers": [phone],
        "linkPrecedence": link_precedence,
        "secondaryContactIds": []
    }
    contacts.append(new_contact)
    return new_contact

def update_contact(existing_contact, email, phone):
    if email not in existing_contact["emails"]:
        existing_contact["emails"].append(email)
    if phone not in existing_contact["phoneNumbers"]:
        existing_contact["phoneNumbers"].append(phone)

@app.route('/identify', methods=['POST'])
def identify_contact():
    data = request.json
    email = data.get('email')
    phone = data.get('phoneNumber')

    existing_contact = find_contact(email, phone)

    if existing_contact is None:
        # Scenario 2: Create a new "Contact" entry
        new_contact = create_contact(email, phone)
        return jsonify(new_contact), 200

    # Scenario 4: Update existing contact and create "secondary" entry
    update_contact(existing_contact, email, phone)
    secondary_contact = create_contact(email, phone, link_precedence="secondary")
    existing_contact["secondaryContactIds"].append(secondary_contact["contactId"])

    return jsonify({
        "primaryContactId": existing_contact["contactId"],
        "emails": existing_contact["emails"],
        "phoneNumbers": existing_contact["phoneNumbers"],
        "secondaryContactIds": existing_contact["secondaryContactIds"]
    }), 200

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": "An unexpected error occurred"}), 400

if __name__ == '__main__':
    app.run(debug=True)
