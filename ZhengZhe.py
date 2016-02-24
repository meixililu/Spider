# encoding urf-8
import re



name = '你地阿迪达斯,As the balance of nature 100 was destroyed and the weather was getting $100.221 warmer and warmer, pandas became less.'
# print(re.findall(r'\d+\.?\d*',name))
# print(re.findall(r'a',name))
chinaeseStr = re.match(ur".*[\u4e00-\u9fa5]+",name)
print(re.findall(r'[\u4e00-\u9fa5]+',name))

















