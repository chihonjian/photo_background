import os
from PIL import Image
import requests
import time
import json

#获取目标所有图片,并完成转化
def get_image():
    global password_count
    password_count = 0
    with open('./config.json') as file_json:
        config=json.load(file_json)
    for item in os.listdir('./photo'):
        print("----正在裁剪[%s]背景色----"%(item))
        for items in config['data']:
            if (items['status'] == 1):
                password_count += 1
            else:
                break
        res=imageClipping(item,config['data'][password_count]['password'])
        if res == 'success':
            print("[%s]裁剪成功"%(item))
            os.remove('./photo/'+item)
        else:
            print("[%s]裁剪失败"%(item))
        time.sleep(1)

#抠图
def imageClipping(path,password):
    try:
        old = './photo/' + path
        new = './temporary/' + path[:-4] + '.png'

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(old, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': password},
        )
        if response.status_code == requests.codes.ok:
            with open(new, 'wb') as out:
                out.write(response.content)
            return 'success'
        else:
            #状态码为402时没有余额
            print("Error:", response.status_code, response.text)
            return 'error'
    except:
        return 'error'


#更换底色
def replaceImage(color = 'red'):
    for item in os.listdir('./temporary'):
        try:
            no_bg_image_path = './temporary/'+item
            no_bg_image = Image.open(no_bg_image_path)
            x, y = no_bg_image.size
            new_image = Image.new('RGBA', no_bg_image.size, color=color)
            new_image.paste(no_bg_image, (0, 0, x, y), no_bg_image)
            new_image.save('./new_photo/'+item)
            print("[%s]换底成功,颜色变更为:[%s]"%(item,color))
        except:
            print("[%s]换底失败" % (item))
            continue

    print("--------------照片已完成转换---------")


def main(color):
    get_image()
    print("图像已裁剪完成,正在更换目标底色")
    replaceImage(color)

if __name__ == '__main__':
    with open('./config.json') as file_json:
        config=json.load(file_json)
    print(config['data'][0])
    while(1):
        print("""
            ------------------自动化证件照底色更换工具---------------------
            ------------------       作者:小健       ----------------------
            ------------------      注意事项         ----------------------
            ------------请将需要更换的图片放置[photo]文件夹中---------------
            ------------生成后的图片位置:[new_photo]文件夹中----------------
            ------------抠图后的人像文件位于:[temporary]文件夹--------------
            ------------如需需要，则保存，否则建议删除 ---------------------
        """)
        item = input("1.照片底色更换 2.清空temporary\n")
        if(item == '1'):
            while(1):
                color = input("输入选项需要的底色:1.红色 2.蓝色 3.白色 4.上一级\n")
                if(color == '1'):
                    main('red')
                    break
                elif(color == '2'):
                    main('blue')
                    break
                elif(color == '3'):
                    main('white')
                    break
                elif(color == '4'):
                    break
                else:
                    print("输入有误，请重新选择")
                    continue




