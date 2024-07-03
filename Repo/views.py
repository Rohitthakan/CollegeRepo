import requests
import uuid
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from Repo.models import Question, Contact, ConfirmationData
from django.core.mail import EmailMessage
from django.contrib import messages
# from django.urls import reverse
from django.core.files.base import ContentFile

# Create your views here.
def index(request):
    return render(request, 'index.html')

def resources(request):
    br = request.POST.get('branch')
    sem = request.POST.get('semester')
    type_exam = request.POST.get('exam_type')
    documents = Question.objects.all()
    if br or sem or type_exam:
        if br:
            documents = documents.filter(branch=br)

        if sem:
            documents = documents.filter(semester=sem)

        if type_exam:
            documents = documents.filter(exam_type=type_exam)
    else:
        documents = documents.order_by('-time')[15:22]

    context = {'document' : documents}
    return render(request, 'resources.html', context)


def verify_email_with_abstract(email):
    api_url = f"https://emailvalidation.abstractapi.com/v1/?api_key=e7b9d4e88c1141948d891902406fe70a&email={email}"
    response = requests.get(api_url)
    result = response.json()
    return result.get('deliverability') == 'DELIVERABLE', result


def send_confirmation_email(branch, semester, subject, exam_type, document, user_email):
    token = uuid.uuid4().hex

    save_confirmation_data(token, branch, semester, subject, exam_type, document, user_email)

    confirmation_url = f"https://collegerepository.pythonanywhere.com/confirm_upload/{token}/"

    document_content = document.read()
    document.seek(0)

    emailmsg = EmailMessage(
        subject='New Question Paper Upload - Confirmation Required',
        body=f'Branch: {branch}\nSemester: {semester}\nSubject: {subject}\nExam Type: {exam_type}\nDocument: {document}\n\n'
             f'Click here to confirm: {confirmation_url}',
        to=['collegerepo2023@gmail.com'],
    )
    emailmsg.attach(document.name, document_content, document.content_type)
    emailmsg.send()


def save_confirmation_data(token, branch, semester, subject, exam_type, document, user_email):
    confirmation_data, created = ConfirmationData.objects.get_or_create(token=token)

    document_content = document.read()
    document.seek(0)
    saved_document = ContentFile(document_content, document.name)

    confirmation_data.branch = branch
    confirmation_data.semester = semester
    confirmation_data.subject = subject
    confirmation_data.exam_type = exam_type
    # confirmation_data.document = document
    confirmation_data.document.save(document.name, saved_document)
    confirmation_data.user_email = user_email

    confirmation_data.save()

def confirm_upload(request, token):
    try:
        confirmation_data = ConfirmationData.objects.get(token=token)
    except ConfirmationData.DoesNotExist:
        messages.error(request, 'Invalid confirmation link. Please contact support.')
        return redirect('add')

    ins = Question(email='collegerepo2023@gmail.com', branch=confirmation_data.branch, semester=confirmation_data.semester, subject=confirmation_data.subject, exam_type=confirmation_data.exam_type, document=confirmation_data.document)
    ins.save()

    user_emailmsg = EmailMessage(
        subject='Question Paper Added Successfully',
        body='Your question paper has been added on CollegeRepository. Thank you for contributing to the CollegeRepository.',
        to=[confirmation_data.user_email],
        from_email='collegerepo2023@gmail.com'
    )
    user_emailmsg.send()

    messages.success(request, 'Question paper added successfully!')
    return redirect('add')


def add(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        branch = request.POST.get("branch")
        semester = request.POST.get("semester")
        subject = request.POST.get("subject")
        exam_type = request.POST.get("exam_type")
        document = request.FILES.get("document")

        is_deliverable, result = verify_email_with_abstract(email)
        if is_deliverable:
            send_confirmation_email(branch, semester, subject, exam_type, document, email)

            messages.success(request, 'Your Request For Adding Question Paper Has Been Sent')
            return redirect('add')
        else:
            messages.error(request, 'Invalid email address. Please try again.')
            return render(request, 'add.html', {'error': 'Invalid email address. Please try again.'})

    return render(request, 'add.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        is_deliverable, result = verify_email_with_abstract(email)
        if is_deliverable:
            contactmsg = EmailMessage(
                subject='Connection Request From College Repository',
                body=f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {desc}',
                to=['collegerepo2023@gmail.com'],
            )
            contactmsg.send()
            ins = Contact(name=name, email=email, phone=phone, desc=desc)
            ins.save()
            messages.success(request, 'Your message was sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Invalid email address. Please try again.')
            return render(request, 'contact.html')

    return render(request, 'contact.html')
