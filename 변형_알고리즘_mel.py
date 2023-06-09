# -*- coding: utf-8 -*-
"""변형 알고리즘 mel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CF36zIwcheAwyAGm55WIl-VMUA16BUBB

코랩에서 먼저 구글 드라이브를 임포트 해줍니다!
"""

from google.colab import drive
drive.mount('/content/gdrive')

"""파일 위치를 확인해줍니다"""

!ls /content/gdrive/MyDrive/Deep_Learning/DNA_Project/Datasets/dataset/door

"""음향 데이터들을 처리하겠습니다.
저희 프로젝트 음향 데이터 자르는 기준은 5초이므로 5초 단위로 잘라주겠습니다. 
"""

# 음향 데이터셋이 저장된 디렉토리 경로
audio_dir = '/content/gdrive/MyDrive/Deep_Learning/DNA_Project/Datasets/pre_process_data'

# 이미지 데이터셋을 저장할 디렉토리 경로
img_dir = '/content/gdrive/MyDrive/Deep_Learning/DNA_Project/Datasets/dataset/door'

# npy 데이터셋을 저장할 디렉토리 경로
npy_dir = '/content/gdrive/MyDrive/Deep_Learning/DNA_Project/Datasets/dataset/door'

"""밑에껀 수정하지 말아주세요!"""

import sklearn
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os


# 각 음향 데이터를 5초씩 단위로 자를 길이 (음향 데이터는 16kHz의 sampling rate를 가짐)
segment_length = 16000 * 5

# mel-spectrogram을 추출하기 위한 파라미터 설정
n_fft = 640
hop_length = 160
n_mels = 128


# 데이터셋 폴더에서 모든 파일 목록을 가져온다
file_list = os.listdir(audio_dir)

for file_name in file_list:
    # 파일 경로를 생성한다
    file_path = os.path.join(audio_dir, file_name)
    
    # 파일이 음향 파일이 아닐 경우 무시한다
    if not file_path.endswith(".wav"):
        continue
    
    # 파일을 불러온다
    signal, sr = librosa.load(file_path, sr=16000)
    
    # 음향 데이터가 5초보다 짧으면, 처음부터 끝까지 추출한다
    if len(signal) < segment_length:
        segments = [signal]
    else:
        # 5초 단위로 음향 데이터를 자른다
        segments = librosa.util.frame(x = signal, frame_length = segment_length, hop_length = (segment_length // 2)).T

    for i, segment in enumerate(segments):
        # mel-spectrogram을 추출한다
        mel_spec = librosa.feature.melspectrogram(y = segment, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)

        # preprocessing
        mel_spec = sklearn.preprocessing.scale(mel_spec, axis=1)
    
        # 추출된 mel-spectrogram을 dB scale로 변환한다
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
        # 시각화한다
        librosa.display.specshow(mel_spec_db, cmap='gray')
        plt.axis('off')
        plt.gca().set_position([0, 0, 1, 1])
    
        # 이미지 파일 경로를 생성한다
        img_file_name = f"{file_name}_{i}.png"
        img_path = os.path.join(img_dir, img_file_name)
    
        # 이미지를 저장한다
        plt.savefig(img_path, bbox_inches=None, pad_inches=0)
    
        # 이미지 출력을 초기화한다
        plt.clf()