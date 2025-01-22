import json
import os

# Set the path to your FFmpeg binary
ffmpeg_bin = r"D:\Tools\ffmpeg\ffmpeg\bin\ffmpeg.exe"
os.environ["FFMPEG_BINARY"] = ffmpeg_bin
from moviepy import VideoFileClip


class MediaProcessor:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as file:
                self.config = json.load(file)
                self.ffmpeg_bin = self.config["ffmpeg_bin"]
                self.video_file = self.config["input_file"]
                self.audio_output = self.config["audio_output_file"]
                self.video_output = self.config["video_output_file"]
                self.target_resolution = tuple(
                    self.config.get("target_resolution", (640, 360))
                )

                # Set FFmpeg environment variable
                os.environ["FFMPEG_BINARY"] = self.ffmpeg_bin
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")

    def extract_audio(self):
        try:
            print(f"Processing {self.video_file} for audio extraction...")
            video = VideoFileClip(self.video_file)
            video.audio.write_audiofile(self.audio_output)
            print(f"Audio extracted and saved to {self.audio_output}")
        except Exception as e:
            print(f"An error occurred during audio extraction: {e}")

    def reduce_video_quality(self):
        try:
            print(f"Processing {self.video_file} for video quality reduction...")
            video = VideoFileClip(self.video_file)
            reduced_video = video.resize(newsize=self.target_resolution)  # Resize video
            reduced_video.write_videofile(
                self.video_output, codec="libx264", audio_codec="aac"
            )
            print(f"Video saved with reduced quality to {self.video_output}")
        except Exception as e:
            print(f"An error occurred during video processing: {e}")


if __name__ == "__main__":
    # Path to JSON configuration file
    config_file_path = r"src\files.json"

    # Create an instance of the class
    processor = MediaProcessor(config_file_path)

    # Extract audio
    processor.extract_audio()

    # Reduce video quality
    processor.reduce_video_quality()
