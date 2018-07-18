import os, subprocess, sys

def ffmpeg_handler():
    check_for_ffmpeg_command = ["which", "ffmpeg"]
    install_ffmpeg_command = ["sudo", "apt-get", "install", "-y", "ffmpeg"]
    if subprocess.run(check_for_ffmpeg_command).returncode != 0:
        subprocess.run(install_ffmpeg_command)

def mkdirs(silence_dir):
    if not os.path.isdir(silence_dir):
        os.mkdir(silence_dir)

def split_audio(bgn_dir, silence_dir):
    for file in [f for f in os.listdir(bgn_dir) if f.endswith(extension)]:
        filename = file[:-len(extension)]
        filepath = os.path.join(bgn_dir, file)
        clippath = os.path.join(silence_dir, filename)
        command = ["ffmpeg", "-i", filepath, "-f", "segment", "-segment_time", "1", "-c", "copy", "{}_%03d.wav".format(clippath)]
        subprocess.run(command)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        root_dir = sys.argv[1]
        background_noise_dir = os.path.join(root_dir, "_background_noise_")
        silence_audio_dir = os.path.join(root_dir, "silence")
        extension = ".wav"
        ffmpeg_handler()
        mkdirs(silence_audio_dir)
        split_audio(background_noise_dir, silence_audio_dir)
    else:
        print("ERROR: Incorrect inputs\n\tusage: python process_background_noise.py <training_audio_directory>")