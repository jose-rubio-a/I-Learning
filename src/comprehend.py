import tkinter as tk
import boto3

root = tk.Tk()
root.geometry("400x240")
root.title("Analisis de sentimiento")
textExample=tk.Text(root,height=10)
textExample.pack()
def getText():
    aws_mag_con=boto3.session.Session(profile_name="demo2")
    client=aws_mag_con.client(service_name='comprehend',  region_name="us-east-1")

    result=textExample.get("1.0", "end")
    print(result)
    response = client.detect_sentiment(Text=result,LanguageCode='es')
    print("Resultado de Análisis:", response['Sentiment'])
    print(response)

    response2 = client.detect_dominant_language(Text=result)
    dominant_language = response2["Languages"][0]["LanguageCode"]
    confidence = response2["Languages"][0]["Score"]
    print(response2)
    print(f"Dominant Language: {dominant_language}")
    print(f"Confidence: {confidence}")

    



btnRead=tk.Button(root,height=1,width=10, text="Analizar",command=getText)
btnRead.pack()
root.mainloop()