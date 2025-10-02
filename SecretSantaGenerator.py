import random
import json
import smtplib
from email.utils import parseaddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def generate_pairs(count):
    while True:
        nums = random.sample(range(count), count)
        if all(i != nums[i] for i in range(count)):
            return nums

def print_pairs(pairs):
     # For debugging purposes only
     for person, partner in pairs.items():
            print(f"{person: <8}:  {partner}")

def send_email(pairs, sender_email, sender_password, player_email_map, email_header, email_msg):
    fromaddr = sender_email
    updated_email_msg = email_msg.replace('\n', '<br>')
    for person, partner in pairs.items(): 
        toaddr = player_email_map[person]
        body_text = f"""\
        <html>
            <body>
                <h1>Hello {person}! 2025 na and it's time for our yearly exchange gift!</h1>
                <h3>{updated_email_msg}</h3>
                <h1>And your partner is...</h1>
                <div style="text-align:center;padding-top: 60px;">
                    <img id="myImage" src="cid:image1" alt="Embedded Image" style="padding: 30px; width: 1200px; height: auto;">
                </div>
            </body>
        </html>
        """
        msg = MIMEMultipart("related")
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = email_header

        msg_alt = MIMEMultipart("alternative")
        msg.attach(msg_alt)
        msg_alt.attach(MIMEText(body_text, 'html'))

        with open(f"{partner}.jpg", "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<image1>')
            img.add_header('Content-Disposition', 'inline', filename='image.jpg')
            msg.attach(img)

        login_user = sender_email.split("@")[0]
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(login_user, sender_password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.close()

def validate_json_data(json_data: dict):
    fields = ["sender_email", "sender_password", "player_count", "players", "email_header", "email_msg"]
    for field in fields:
        if field not in json_data:
            print(f"ERROR: JSON file must contain '{field}'")
            exit(1)
    
    if "@" not in parseaddr(json_data["sender_email"])[1]:
            print(f"ERROR: email address: {json_data['sender_email']} is not valid.")
            exit(1)

    player_count = json_data['player_count']
    player_details = json_data['players']
    if len(player_details) != player_count:
        print(f"ERROR: Invalid JSON file: players should have length of player_count ({player_count})")
        exit(1)
    for player_info in player_details:
        if "name" not in player_info or "email" not in player_info:
            print(f"ERROR: each person must have a name and email address")
            exit(1)
        if "@" not in parseaddr(player_info["email"])[1]:
            print(f"ERROR: email address: {player_info['email']} is not valid.")
            exit(1)


if __name__ == "__main__":
    json_file = input("Enter JSON file: ")
    try:
        with open(json_file, "r") as f:
            json_data = json.load(f)
    except IOError:
        print(f"ERROR: {json_file} does not exist!")
        exit(1)
    
    validate_json_data(json_data)
    sender_email = json_data['sender_email']
    sender_password = json_data['sender_password']
    num_players = json_data['player_count']
    players = json_data['players']
    email_header = json_data['email_header']
    email_msg = json_data['email_msg']
    names = [item['name'] for item in players]
    player_email_map = {item['name'] : item['email'] for item in players}
    
    partners = generate_pairs(num_players)
    pairs = {names[i] : names[partners[i]] for i in range(num_players)}

    send_email(pairs, sender_email, sender_password, player_email_map, email_header, email_msg)
