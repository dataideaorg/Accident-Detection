import pathlib
from django.shortcuts import render
from .props import Model, colored


# django rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ClassificationSerializer


# Create your views here.
BASE_DIR = pathlib.Path(__file__).resolve().parent

try:
    model = Model()
    model.load(BASE_DIR / 'models/acc_modelv2.h5')
    print(colored(0, 0, 255, "Successfully loaded the model"))
except Exception as e:
    print(colored(255, 0, 0, f"An error occured while loading the model {str()}"))


@api_view(['GET', 'POST'])
def classify(request):
    if request.method == 'POST':
        try: 
            image_file = request.FILES['image']
            image_array = model.process_image(image_file)
            predictions = model.predict(image_array)
            prediction = model.predicted_class(predictions)
            confidence = model.confidence(predictions)
            serializer = ClassificationSerializer({
                'prediction': int(prediction),
                'confidence': round(confidence, 3),
            })

            print(colored(0, 0, 255,f'{str(serializer.data)}'))
            return Response(serializer.data)
        except Exception as e:
            print(colored(255, 0, 0, f'An error occured during classification {str(e)}'))
            serializer = ClassificationSerializer({
                'prediction': 999,
                'confidence': 999,
            })
            return Response(serializer.data)