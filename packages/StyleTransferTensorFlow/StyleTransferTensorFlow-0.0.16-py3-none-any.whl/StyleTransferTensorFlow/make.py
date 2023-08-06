import os

def MakeVideo(vidpath, style_image_path):
  current_directory = os.getcwd()
  onlyfiles, imgfolderpath = st.extract.ExtractFrames(vidpath, current_directory)
  content_img_path_list = [os.path.join(imgfolderpath, pp) for pp in onlyfiles]
  #style_image_path = os.path.join(os.getcwd(),'style.jpg')
  generated_img_list_output = st.style.StyleTransferVideo(content_img_path_list, style_image_path)
  final_cv2_image_list = st.convert.ConvertTensorToCV2(generated_img_list_output)
  avi_video_path = st.convert.ConvertImagesToVideo(final_cv2_image_list)
  mp4_video_path = st.convert.convert_avi_to_mp4(avi_video_path)