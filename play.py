import logging
import asyncio
import os 
import sys
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from aiortc.contrib.media import MediaPlayer
import pyttsx3

# Enable logging for debugging
logging.basicConfig(level=logging.ERROR)

async def main():
    
    try:
        # Choose a connection method (uncomment the correct one)
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip="192.168.8.181")
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, serialNumber="B42D4000O9U7MN81")
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.Remote, serialNumber="B42D2000XXXXXXXX", username="email@gmail.com", password="pass")
        conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)
        
        await conn.connect()

        engine = pyttsx3.init()

        engine.save_to_file(input() * 20, 'curr.mp3', )
        
        print("A")

        engine.runAndWait()

        print("B")

        await asyncio.sleep(3)

        print("C")
        
        mp3_path = os.path.join(os.path.dirname(__file__), "curr.mp3")
        
        track = MediaPlayer(mp3_path).audio
        print(type(track))
        conn.pc.addTrack(track)




        await asyncio.sleep(3600)  # Keep the program running to handle events

    except ValueError as e:
        # Log any value errors that occur during the process.
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

