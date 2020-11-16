# amazon-electronics-review-sentiments-tf

### how to execute
echo {"text":"I am extremely happy and satisfied with this great Bose Home Speaker 300. The quality sound production of this speaker is absolutely fantastic, and the speaker has great bass. The speaker looks nice, neat and attractive. Easy to set up with Bluetooth. Brilliant! Worth every penny. Thankyou Bose! You've done a geat Job, Bose, 10 out of 10!"} | curl -i  -H "Content-Type: application/json" -d @- http://127.0.0.1:5000/seclassifier


### check the health status
curl "http://127.0.0.1:5000/healthcheck"



### after scaling up with waitress, use the following command
echo {"text":"I liked that alexa and amazon music are both easy to set up using the bose mobile app. The sound quality is 10 out of 10 and the volume packs a punch! This device is mostly used for listening to news, weather music playlists, timers and alarms and of course, asking alexa ridiculous questions for the lol! Love this speaker, and highly recommend!"} | curl -i  -H "Content-Type: application/json" -d @- http://machinename.xxx.xxx.com:8000/seclassifier

