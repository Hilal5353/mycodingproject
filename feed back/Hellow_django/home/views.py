from django.shortcuts import render, redirect
from .models import CustomerFeedback, CustomerResponse, Option
# Create your views here.


def index(request):
    feed_back = CustomerFeedback.objects.all()
    return render(request, 'home/survey.html', {'feedback':feed_back})




def customer_feedback(request, id):
    feed_back = CustomerFeedback.objects.get(id = id)
    if request.method == 'POST':
        for question in feed_back.question.all():
            response_text = request.POST.get(f"response_{question.id}")
            selected_options_ids = request.POST.getlist(f"option_{question.id}")
            print("this .....", response_text)
            print("this is select option", selected_options_ids)
            
            response = CustomerResponse.objects.create(
                feeedback  = feed_back,
                question = question,
                response_text = response_text if question.question_type in ['text', "BigText"] else None
            )

            if selected_options_ids:
                selected_options = Option.objects.filter(id__in = selected_options_ids)
                response.selected_option.set(selected_options)
            
        return redirect('/thankyou/')

    
    return render(request, 'home/customer_feedback.html', {'questions':feed_back.question.all()})


def thankyou(request):
    return render(request, 'home/thankyou.html')

