from django.db import models

# Create your models here.
class Questions(models.Model):
    QUESTION_CHOICES = (("text", "text"), ("BigText", "BigText"), ("Radio", "Radio"), ("Checkbox", "Checkbox"))
  
    question = models.CharField(max_length=100)
    question_type = models.CharField(choices=QUESTION_CHOICES, max_length=50, default=True)
    
    def __str__(self) -> str:
        return f"{self.question}  {self.question_type }"
    
class Option(models.Model):
    option = models.ForeignKey(Questions, related_name="options", on_delete=models.CASCADE)
    option_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f"{self.option.question} {self.option_name}"
    
class CustomerFeedback(models.Model):
    question = models.ManyToManyField(Questions)
    survey_name = models.CharField(max_length=100, default='Default Survey Name')

    def __str__(self):
        return self.survey_name
    
    
class CustomerResponse(models.Model):
    feeedback = models.ForeignKey(CustomerFeedback, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    response_text = models.TextField(null=True, blank=True)
    selected_option = models.ManyToManyField(Option, blank=True)


    def __str__(self) -> str:
        return f"{self.question}"




