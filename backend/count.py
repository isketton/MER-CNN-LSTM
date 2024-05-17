import os
import random


    
file_count = len([name for name in os.listdir('/Users/isiahketton/Downloads/PMEmo2019/chorus/wav/q2') if os.path.isfile(os.path.join('/Users/isiahketton/Downloads/PMEmo2019/chorus/wav/q2', name))])
print(file_count)

