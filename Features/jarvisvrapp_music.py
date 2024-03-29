import pygame
import threading

class MusicPlayer:
    def play_music_thread(self):
        music_thread = threading.Thread(target=self.play_music)
        music_thread.start()

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_music(self):
        pygame.init()
        pygame.mixer.init()

        # Add the path to your favorite songs
        playlist = [
            # Add desired songs with the following path model here
            #r"C:\Users\alexandru.filcu\Downloads\Y2meta.app - Mylo Vs Miami Sound Machine - Doctor Pressure (128 kbps).mp3",
            #r"C:\Users\alexandru.filcu\Downloads\Y2meta.app - Cargo - Aproape De Voi (128 kbps).mp3"
            # Add more songs as needed
        ]

        for song in playlist:
            try:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                print(f"Now playing: {song}")
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except pygame.error as e:
                print(f"Error: {e}")
                print(f"Skipping {song}. Make sure the file path is correct and the file is a valid music file.")
