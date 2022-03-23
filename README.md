# BastionPi
Code to support a Raspberry Pi as a bastion host for a homelab

Install DietPi with just Dropbear as the SSH server. Then install and configure ngrok (https://ngrok.com)  

Connect a resistor and LED to P0  
Connect a button to P1  

Add the Python scripts to /opt/homelab and copy the .service files to /etc/systemd/system/  

Then do the following:  
```systemctl daemon-reload
systemctl enable ngrok
systemctl start ngrok
systemctl enable ssh-monitor
systemctl start ssh-monitor
echo "nothing yet" > /opt/homelab/ngrok.last
echo "*/5 * * * * root cd /opt/homelab; /usr/bin/python3 /opt/homelab/check-ngrok.py" > /etc/cron.d/check-ngrok
```

When there are live SSH sessions via the ngrok tunnel, the LED will be lit.  
When the button is pressed, all SSH sessions via the ngrok tunnel are disconnected.
