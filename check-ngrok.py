import requests, hashlib

# define mailgun function
def send_simple_message(message):
    return requests.post(
        "https://api.eu.mailgun.net/v3/[DOMAIN]/messages",
        auth=("api", "APIKEY"),
        data={"from": "Homelab <ngrok-monitor@[DOMAIN]>",
              "to": ["EMAIL ADDRESS"],
              "subject": "NGROK SSH Tunnel Update",
              "text": message})

# get the tunnel information
response = requests.get('http://localhost:4040/api/tunnels')
jsonResponse = response.json()
message = jsonResponse['tunnels'][0]['public_url']

# read the stored data
with open('ngrok.last', 'r') as file:
    data = file.read().rstrip()

# hash and compare the stored and retrieved
last = hashlib.md5(data.encode())
current = hashlib.md5(message.encode())

if current.hexdigest() != last.hexdigest():
  # write the new data
  f = open("ngrok.last", "w")
  f.write(message)
  f.close()
  # tidy up the data
  message = message.replace('tcp://', 'Host: ')
  message = message.replace('.io:', '.io Port: ')
  # send an email via mailgun
  send_simple_message(message)
