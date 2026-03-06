from google import genai
import time
import argparse
from dotenv import load_dotenv
import os

# This script demonstrates how to use the Google Gemini API for video understanding tasks.
# Put videos in vlm-pref/demos
# SPECIFICATIONS:
# Run the script in the vlm-pref folder
# If you want a default API key, please create a .env file in the vlm-pref/scripts folder and add your key as GOOGLE_API_KEY=your_api_key

def wait_for_active(client, video_file):
    while video_file.state.name != "ACTIVE":
        print(f"Waiting for {video_file.name} to become ACTIVE...")
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)
    return video_file


def main(api_key):
    parser = argparse.ArgumentParser(description="Google AI preference label inference between two videos")

    # Add args
    parser.add_argument("--api_key", type=str, default=api_key,
                        help="put your api key")
    parser.add_argument("--model", type=str, default="gemini-3.1-pro-preview",
                        help="which model to use (e.g. gemini-3-flash-preview)")
    parser.add_argument("--video_path_1", type=str, default="demos/bad_shaky_agentview.mp4",
                        help="path to the first video")
    parser.add_argument("--video_path_2", type=str, default="demos/good_clean_medium_agentview.mp4",
                        help="path to the second video")
    parser.add_argument("--prompt", type=str, default=None,
                        help="text prompt to help the vlm (if unspecified, will use prompt in the txt file)")
    args = parser.parse_args()

    client = genai.Client(api_key=args.api_key)

    print("Uploading videos...")
    video_file_1 = client.files.upload(file=args.video_path_1)
    video_file_2 = client.files.upload(file=args.video_path_2)

    prompt = args.prompt
    if prompt is None:
        with open("scripts/vlm_prompt_preference_labels.txt", 'r') as f:
            prompt = f.read()

    video_file_1 = wait_for_active(client, video_file_1)
    video_file_2 = wait_for_active(client, video_file_2)

    response = client.models.generate_content(
        model=args.model,
        contents=[
            "Video 1:", video_file_1,
            "Video 2:", video_file_2,
            prompt
        ]
    )

    print(response.text)

if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    main(api_key)