import subprocess 
cmd="python inference.py --checkpoint_path wav2lip_gan.pth  --face Images/swatishinde.jpg --audio Audio/Pitch.mp3"

p=subprocess.Popen(cmd,shell=True)
out,err  = p.communicate()
print(err)
print(out)