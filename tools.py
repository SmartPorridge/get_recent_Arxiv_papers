import os,time
from translate import Translator
from googletrans import Translator as Google_Translator
from PIL import Image
from urllib import request,parse
import json



def translate_google(src, dest='zh-CN',cn_host=False):
    if cn_host:
        translate = Google_Translator(service_urls=[
        'translate.google.cn',
    ])
    else:
        translate = Google_Translator()
    return translate.translate(src,dest=dest).text

def translate(src, dest='zh-CN'):
    translator = Translator(to_lang="chinese")
    translation = translator.translate(src)
    return translation

def translate_baidu(content):
    url = "http://fanyi.baidu.com/sug"
    data = parse.urlencode({"kw":content})  # 将参数进行转码
    headers = {
        'User-Agent': 'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'
    }
    req = request.Request(url,data=bytes(data,encoding="utf-8"),headers=headers)
    r = request.urlopen(req)
    # print(r.code)  查看返回的状态码
    html = r.read().decode('utf-8')
    # json格式化
    html = json.loads(html)
    # print(html)
    for k in html["data"]:
        print(k["k"],k["v"])

def get_element_snapshot(driver, element, pad = 0):
    # 保存当前结果页面
    driver.save_screenshot("./tmp/temp.png")

    # 保存element的截图
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']

    #print(left, top, right, bottom)
    im = Image.open("./tmp/temp.png")
    im = im.crop((left - pad, top - pad, right + pad, bottom + pad))
    os.remove("./tmp/temp.png")
    return im

if __name__ == "__main__":
    text = 'Cardiac image segmentation is a critical process for generating personalized models of the heart and for quantifying cardiac performance parameters. Several convolutional neural network (CNN) architectures have been proposed to segment the heart chambers from cardiac cine MR images. Here we propose a multi-task learning (MTL)-based regularization framework for cardiac MR image segmentation. The network is trained to perform the main task of semantic segmentation, along with a simultaneous, auxiliary task of pixel-wise distance map regression. The proposed distance map regularizer is a decoder network added to the bottleneck layer of an existing CNN architecture, facilitating the network to learn robust global features. The regularizer block is removed after training, so that the original number of network parameters does not change. We show that the proposed regularization method improves both binary and multi-class segmentation performance over the corresponding state-of-the-art CNN architectures on two publicly available cardiac cine MRI datasets, obtaining average dice coefficient of 0.84'
    b = translate_google(text,cn_host=True)
    print(b)
