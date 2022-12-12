import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
from cloud.stemming import string_stream_stem
import base64
from io import BytesIO
import cv2

# Convert Image to Base64 
def im_2_b64(image):
    # buff = BytesIO()
    # image.save(buff, format="JPEG")
    # img_str = base64.b64encode(buff.getvalue())
    # img_str = str(img_str, "utf-8")
    # cv2.imwrite("temp.jpg", image)
    image.to_file("temp.jpg")
    fp = open("temp.jpg", "rb")
    img_str = fp.read()
    fp.close()
    return img_str

def tcg(texts):
    cut = jieba.cut(texts)  #分词
    string = ' '.join(cut)
    return string

def make_cloud_img(text, threashold=5):
    mask = np.array(Image.open('cloud/0background.jpg'))
    image_colors = ImageColorGenerator(mask) # 从图片提取颜色

    # font = 'cloud/SKTAITI.TTF'
    font = "cloud/Thin.ttf"
    # font = "cloud/Song.ttf"
    
    # string=tcg(text)
    # print(string)
    (w_map, stem_string) = string_stream_stem(text, threashold)
    if(len(stem_string) < 5):
        stem_string += "(Insufficient Issues)"

    img = Image.open('cloud/Octocat.jpg') 
    img_array = np.array(img) 
    stopword=['', 
        "debug",
        "test",
        "fx",
        "fix",
        "use",
        "build",
        "issue",
        "issu",
        "build",
        "remove",
        "remov",
        "add",
        "delete",
        "delet",
        "update",
        "updat"
    ]  
    wc = WordCloud(
        background_color='white',
        width=800,
        height=600,
        mask=img_array, 
        font_path=font,
        stopwords=stopword,
        color_func=image_colors
    )
    wc.generate_from_text(stem_string)#绘制图片
    # print(w_map) # 输出单词出现频率
    # sys = w_map
    # new_sys1 = sorted(sys.values())
    # print(new_sys1)

    # 打印出根据value排序后的键值对的具体值

    # print(new_sys2)
    # print(stem_string)
    # plt.imshow(wc)
    # plt.axis('off')
    # plt.show()  #显示图片
    # wc.to_file('beautifulcloud.jpg')  #保存图片
    return (wc, w_map)


