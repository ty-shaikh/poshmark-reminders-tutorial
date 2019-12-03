import pickle
from html2text import html2text
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

USER_EMAIL = "PERSONAL_ACCOUNT@gmail.com"

def generate_markup(title, collection):
    "Generate email markup from recent items"
    html = "<div style='text-align: center;'>"
    heading = f'<p style="font-size: 1.5rem; font-weight: bold;">{title}&nbsp;<span style="font-size: 1rem;">({len(collection)} items)</span></p>'
    item_group = ""

    for item in collection:
        title = item[0]
        price = item[1]
        link = "https://poshmark.com" + item[2]
        img = item[3]

        card_element = f'<a style="text-decoration: none;" href="{link}" target="_blank"><div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); width: 300px; margin: 0 auto;"><img src="{img}" style="max-width: 100%"><div style="padding: 2px 16px;"><p style="font-size: 1.3rem; font-weight: bold;">{title} ({price})</p></div></div></a></div><br>'

        item_group += card_element

    html = html + heading + item_group

    return html

recent_items = pickle.load(open("naked_and_famous.p", "rb"))
email_markup = generate_markup("Naked and Famous Jeans", recent_items)

def send_email(items, recipient):
    "Send email through dummy Gmail account"
    sender_email = "DUMMY_ACCOUNT@gmail.com"
    receiver_email = recipient
    password = "DUMMY_ACCOUNT_PASSWORD"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Latest Poshmark Listings"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html = """    <html>
      <body>
      <div style="margin: 0 auto;">
        <!-- Heading -->
        <div>
          <h1 style="text-align: center;">New Poshmark Listings</h1>
          <hr>
        </div>
        <br>
    """ + items + """
      </div>
      </body>
    </html>
    """

    text = html2text(html)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(str(html), "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

send_email(email_markup, USER_EMAIL)
