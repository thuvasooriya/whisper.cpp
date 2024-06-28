import sys
import subprocess
import os


def main():
    # current_path = os.getcwd()
    # if os.path.basename(current_path) != "whisper.cpp":
    #     print("This script must be run from the 'whisper.cpp' directory.")
    #     sys.exit(1)
    if len(sys.argv) >= 2:
        file = sys.argv[1]
        model_name = sys.argv[2] if len(sys.argv) == 3 else "base.en-q5_1"
        fname, model = process_names(file, model_name)
        try:
            result = process(file, fname, model)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Usage: python whisper.py <wav_file> [<model_name>]")


def process(file, fname, model):
    command1 = (
        f"ffmpeg -y -i '{file}' -ar 16000 -ac 1 -c:a pcm_s16le './audio/{fname}.wav'"
    )

    # Execute the command
    # result = subprocess.run(command1, shell=True, capture_output=True, text=True)
    # print(result.stdout)
    process1 = subprocess.Popen(
        command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print("converting file")
    output1, error1 = process1.communicate()
    # if error1:
    #     raise Exception(f"error processing file: {error1.decode('utf-8')}")
    if not os.path.exists(f"audio/{fname}.wav"):
        raise Exception(f"error processing file: {error1.decode('utf-8')}")
    # print(output1)

    if input(f"save to file {fname}.txt? y/n: ") == "y":
        if os.path.exists(f"export/{fname}.txt"):
            raise Exception("file with a same name found")
        command2 = f"./main -m '{model}' -f 'audio/{fname}.wav' -np -nt -otxt -of 'export/{fname}'"
    else:
        command2 = f"./main -m '{model}' -f 'audio/{fname}.wav' -np -nt"

    process2 = subprocess.Popen(
        command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print("transcribing audio...")
    output2, error2 = process2.communicate()

    if error2:
        print(f"Error processing audio: {error2.decode('utf-8')}")

    # Process and return the output string
    decoded_str = output2.decode("utf-8").strip()
    processed_str = decoded_str.replace("[BLANK_AUDIO]", "").strip()

    return processed_str


def process_names(file, model_name):
    print("running automate function")
    if not os.path.exists(file):
        raise FileNotFoundError(f"file not found: {file}")
    if not os.path.exists("export"):
        os.makedirs("export", exist_ok=True)

    model = f"./models/ggml-{model_name}.bin"
    # Check if the file exists
    if not os.path.exists(model):
        raise FileNotFoundError(
            f"Model file not found: {model} \n\nDownload a model with this command:\n\n> bash ./models/download-ggml-model.sh {model_name}\n\n"
        )

    bname = os.path.basename(file)
    fname, fext = os.path.splitext(bname)
    print("file path:", file)
    print("file name:", fname)
    return fname, model


if __name__ == "__main__":
    main()
