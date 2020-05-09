import urllib3, requests, json, datetime

#Generate token using model API key
apikey = "LoziHUyUjG3iS7i5HJDSsCA_RrZflRkkr67-ikRNagq_" 
url     = "https://iam.bluemix.net/oidc/token"
headers = { "Content-Type" : "application/x-www-form-urlencoded" }
data    = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
IBM_cloud_IAM_uid = "bx"
IBM_cloud_IAM_pwd = "bx"
response  = requests.post( url, headers=headers, data=data, auth=( IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd ) )
iam_token = response.json()["access_token"] #IAM token generator


ml_instance_id = "5c206edc-da28-4c23-943a-7c2c3d59caf8" 
header = {"Content-Type": "application/json", "Authorization": "Bearer " + 
            iam_token, "ML-Instance-ID": ml_instance_id}

'''
Manually define and pass the array(s) of values to be scored in the next line.
The array matches the fields in the payload_scoring input.
Vehicle age is the difference of this year and the year the car was released.
'''
array = [104892, "Austin", "TX", "Buick", "VeranoLeather", 4]

payload_scoring = {"input_data": [{"fields": ["Mileage", "City", "State", 
                "Make", "Model", "Vehicle age"], "values": [array]}]}

response_scoring = requests.post(
                "https://eu-gb.ml.cloud.ibm.com/v4/deployments/9df123fa-2846-4f5e-a4ae-d3ce159cb3a0/predictions", 
                json=payload_scoring, headers=header)

arraypred = response_scoring.json()["predictions"][0]["values"][0] #Predicted value of car
now = datetime.datetime.now()
year = (now.year - (array[-1]))

print("Scoring response")
print("The predicted price of a {} in {}, "
        "{} with a mileage of {} and model {} "
        " that was released in {} is {}.".format(array[3], 
                                                array[1], array[2], 
                                                array[0], array[-2], 
                                                year, arraypred))