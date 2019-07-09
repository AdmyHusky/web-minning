import pymongo
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Setting mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
collection = mydb["tweet"]

# initial value
text = ""

# This function will replace word(https, co, RT) to blank
def replaceMultiple(mainString, toBeReplaces, newString):
    for elem in toBeReplaces:
        if elem in mainString:
            mainString = mainString.replace(elem, newString)

    return mainString


# This for-loop will get tweet from mongo to value(text)
for x in collection.find({}, {"text": 1, "_id": 0}):
    tweet = x['text']
    text = text + " " + tweet
    text = replaceMultiple(text, ['https', 'RT', 'co'], '')

# Generate a word cloud image
# ตัดคำพวก stopword เช่น "the", "a", "an", "or", "not", "in"
stopword = set(STOPWORDS)
# เปิดภาพแล้วเก็บภาพเป็น array
shape = np.array(Image.open('google_mask.png'))
colors = ["#FF0000", "#111111", "#101010", "#121212", "#212121", "#222222"]
cmap = LinearSegmentedColormap.from_list("mycmap", colors)

# Word cloud object สำหรับการสร้างภาพและวาดภาพ โดยมีการกำหนด background_color คือสีพื้นหลังสำหรับรูป WordCloud,
# stopwords คือ คำที่เราต้องการกำจัดออกไป, mask คือลักษณะที่จะวาด WordCloud ลงไป, width กว้าง, height ยาว, เซตของสีที่จะใช้
# generate สร้าง WordCloud จาก text
wordcloud = WordCloud(background_color="white",
                      stopwords=stopword, mask=shape, width=1987, height=736, colormap=cmap).generate(text)
# แสดงรูปภาพ wordcloud
plt.imshow(wordcloud, interpolation='bilinear')
# ปิดไม่แสดงเส้นแกน x,y
plt.axis("off")
# แสดงหน้าต่างและรูป
plt.show()
