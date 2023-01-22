from django.shortcuts import render
from Repo.models import Question, Contact
from django.core.mail import EmailMessage
# Create your views here.
def index(request):
    return render(request, 'index.html')

def resources(request):
    br = request.POST.get('branch')
    sem = request.POST.get('semester')
    type_exam = request.POST.get('exam_type')
    if br and sem:
        documents = Question.objects.filter(branch = br, semester = sem, exam_type=type_exam)
    else:
        documents = Question.objects.order_by('-time')[:11]
    context = {'document' : documents}
    return render(request, 'resources.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        contactmsg = EmailMessage(desc, email, to=['rohitthakan2001@gmail.com'])
        contactmsg.send()
        ins = Contact(name=name, email=email, phone=phone, desc=desc)
        ins.save()
    return render(request, 'contact.html')
def add(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        branch = request.POST.get("branch")
        semester = request.POST.get("semester")
        subject = request.POST.get("subject")
        exam_type = request.POST.get("exam_type")
        document = request.FILES.get("document")
        emailmsg = EmailMessage((subject, document), email, to=['collegerepo2023@gmail.com'])
        emailmsg.send()
        ins = Question(email=email, branch=branch, semester=semester, subject=subject, exam_type=exam_type, document=document)
        ins.save()
    return render(request, 'add.html')
