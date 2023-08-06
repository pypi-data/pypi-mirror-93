import cv2

def ExtractFrames(video_path, directory, extractframerate=30):
  vidcap = cv2.VideoCapture(video_path)

  success,image = vidcap.read()
  count = 0

  newpath = os.path.join(directory, 'imgfolder')

  if os.path.exists(newpath):
    shutil.rmtree(newpath)
    
  os.makedirs(newpath)
  
  while success:
    if (count%extractframerate==0):
      cv2.imwrite(os.path.join(newpath, "frame%.6d.jpg" % count), image)     # save frame as JPEG file
    success,image = vidcap.read()
    count += 1 

  frames = [f for f in os.listdir(newpath) if os.path.isfile(os.path.join(newpath, f))]
  frames.sort()
  print("-----------Frame extraction completed-----------")
  return frames, newpath

if __name__ == "__main__":
    import sys
    ExtractFrames(sys.argv[1], sys.argv[2])