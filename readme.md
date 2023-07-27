# Deviant
Deviant: quadruped wheeled robot.<br />
YouTube channel: https://www.youtube.com/channel/UC5iMcYcLpUnzzhuc-a_uPiQ<br />
Email: light.robotics.2020@gmail.com

To run deviant:
- run "python3 /deviant/deviant_hardware/deviant_dualshock.py"
- run "python3 /deviant/run/movement_processor.py"
- run "sudo python3 /deviant/run/neopixel_commands_reader.py"

Video streaming:
- sudo ffmpeg -s 1024x576 -f video4linux2 -i /dev/video0 -f mpegts -codec:v mpeg1video -b:v 4000k -r 30 http://{nexus_ip}:8081/12345/1024/576/

Useful:
- vcgencmd measure_temp
- cat /var/log/syslog.1
