import json
import os

from moviepy.editor import VideoFileClip
from moviepy.video.fx import resize


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
                self.video_output_reduced = self.config["video_output_reduced"]
                self.target_resolution = tuple(
                    self.config.get("target_resolution", (640, 360))
                )

                # Set FFmpeg environment variable
                os.environ["FFMPEG_BINARY"] = self.ffmpeg_bin
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")

    def extract_audio(self):
        """extract only audio from the video"""
        try:
            print(f"Processing {self.video_file} for audio extraction...")
            video = VideoFileClip(self.video_file)
            audio = video.audio
            audio.write_audiofile(self.audio_output)
            print(f"Audio extracted and saved to {self.audio_output}")
        except Exception as e:
            print(f"An error occurred during audio extraction: {e}")

    def reduce_video_quality(self):
        """just reduce the video quality, audio will not be seperated"""
        try:
            print(f"Processing {self.video_file} for video quality reduction...")
            video = VideoFileClip(self.video_file)

            # Reduce video quality by setting a lower bitrate
            video.write_videofile(
                self.video_output,
                codec="libx264",
                audio_codec="aac",
                bitrate="500k",  # Adjust the bitrate as needed
            )
            print(f"Video saved with reduced quality to {self.video_output}")
        except Exception as e:
            print(f"An error occurred during video processing: {e}")

    def separate_video_without_audio(self):
        """separate video without audio and save both"""
        try:
            print(f"Processing {self.video_file} to separate audio and video...")
            video = VideoFileClip(self.video_file)

            # Extract and save the audio
            audio = video.audio
            audio.write_audiofile(self.audio_output)
            print(f"Audio extracted and saved to {self.audio_output}")

            # Remove the audio from the video
            video = video.without_audio()

            # Save the video without audio
            video.write_videofile(self.video_output, codec="libx264")
            print(f"Video saved without audio to {self.video_output}")
        except Exception as e:
            print(f"An error occurred during video processing: {e}")


if __name__ == "__main__":
    # Path to JSON configuration file
    config_file_path = r"src\files.json"

    # Create an instance of the class
    processor = MediaProcessor(config_file_path)

    # Extract audio (optional, if needed)
    # processor.extract_audio()

    # Reduce video quality (optional)
    # processor.reduce_video_quality()

    # Separate video without audio and reduce size
    processor.separate_video_without_audio()
