from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect


def index(request):
    return render(request, 'students/index.html',{
        'students': Student.objects.all()
    })


def view_student(request, id):
    student = Student.objects.get(id=id)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student_number = form.cleaned_data['student_number']
            new_first_name = form.cleaned_data['first_name']  
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_field_of_study = form.cleaned_data['field_of_study']
            new_gpa = form.cleaned_data['gpa']
        
            new_student = Student(
                student_number=new_student_number,
                first_name=new_first_name,
                last_name=new_last_name,
                email=new_email,
                field_of_study=new_field_of_study,
                gpa=new_gpa
            )
            new_student.save()

            return render(request, 'students/add.html', {
                'form': StudentForm(),
                'success': True
            })
    else:
        form = StudentForm()

    return render(request, 'students/add.html', {
        'form': form
    })


@login_required(login_url='login')
def edit(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request,'students/edit.html',{
                'form': form, 
                'success': True 
            })
    else:
        student = Student.objects.get(pk=id)
        form = StudentForm(instance=student)

    return render(request, 'students/edit.html', {
        'form': form
    })


@login_required(login_url='login')
def delete(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        student.delete()

    return HttpResponseRedirect(reverse('index'))
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now login.")
            return redirect('login')  # redirect only after success
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'students/register.html', {'form': form})