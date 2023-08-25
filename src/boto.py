import boto3

translate = boto3.client(service_name='translate', region_name='region', use_ssl=True)

result = translate.translate_text(Text="Hello, World", 
            SourceLanguageCode="en", TargetLanguageCode="de")
print('TranslatedText: ' + result.get('TranslatedText'))
print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))



'''
import boto3

translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

response3=translate.translate_text(Text="Hello word", SourceLanguageCode="en", TargetLanguageCode="es")
print('TranslatedText: ' + response3.get('TranslatedText'))
print('SourceLanguageCode: ' + response3.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + response3.get('TargetLanguageCode'))
'''