####Virtual host####
First CMD
CMD: cd C:\Program Files\mosquitto
CMD: -v
----------------
Second CMD
#CMD is Publisher and GUI is Subscriber
CMD: cd C:\Program Files\mosquitto 
Run code
CMD: mosquitto_pub -t Sub -h localhost -p 1883 -m "15000 8000 48000 8000"
----------------
Third CMD
##CMD is Subscriber and GUI is Publisher
CMD: cd C:\Program Files\mosquitto 
CMD: mosquitto_sub -t test -h localhost -p 1883
Run code
----------------