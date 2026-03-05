from google import genai
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="Google AI inference")

    # Add args
    parser.add_argument("--api_key", type=str, default="",
                        help="put your api key")
    parser.add_argument("--model", type=str, default="",
                        help="which model to use (e.g. gemini-3-flash-preview)")
    parser.add_argument("--video_path", type=str, default="",
                        help="where your video at")
    parser.add_argument("--prompt", type=str, default=None,
                        help="text prompt to help the vlm (if unspecified, will use prompt in the txt file)")
    args = parser.parse_args()

    client = genai.Client(api_key=args.api_key)

    video_file = client.files.upload(file=args.video_path)
    prompt = args.prompt
    if prompt is None:
        with open("vlm_prompt.txt", 'r') as f:
            prompt = f.read()

    while video_file.state.name != "ACTIVE":
        print("Waiting for file to become ACTIVE...")
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)

    response = client.models.generate_content(
        model=args.model,
        contents=[
            video_file,
            prompt
        ]
    )

    print(response.text)


if __name__ == '__main__':
    main()