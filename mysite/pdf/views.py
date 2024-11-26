from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


# Create your views here.

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name',"")
        email = request.POST.get('email',"")
        phone = request.POST.get('phone',"")
        summary = request.POST.get('summary',"")
        degree = request.POST.get('degree',"")
        school = request.POST.get('school',"")
        university = request.POST.get('university',"")
        previous_work = request.POST.get('previous_work',"")
        skills = request.POST.get('skills',"")

        profile  = Profile(name=name , email=email ,phone = phone , summary=summary , degree=degree , school=school , university=university , previous_work = previous_work , skills=skills)
        profile.save()
        
    return render(request, 'pdf/index.html')

def cv(request, id):
    user_profile = Profile.objects.get(pk=id)

    # Render the HTML template
    template = loader.get_template('pdf/cv.html')
    html = template.render({'user_profile': user_profile})

    # Path to wkhtmltopdf executable
    path_to_wkhtmltopdf = r'C:\wkhtmltox\bin\wkhtmltopdf.exe'  # Update this with the correct path

    # Configure pdfkit with the correct path
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    # PDF generation options
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'orientation': 'Portrait',
    }

    # Generate the PDF using the configuration
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Return the PDF as an HTTP response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv.pdf"'

    return response



def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})

