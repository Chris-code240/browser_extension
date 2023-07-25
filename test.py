# import requests

# url = 'http://127.0.0.1:5000/analyze'
# files = {'image': open('static/img/test2.jpg', 'rb')}
# response = requests.post(url, files=files)

# if response.ok:
#     data = response.json()
#     # print("Prediction:", data['prediction'])
#     # print("Message:", data['message'])
#     print(data)
# else:
#     print("Error occurred:", response.json

from image_analyzer import predict_image,load_model

print(predict_image('./static/img/t1.jpeg',load_model('trained_model.joblib')))

