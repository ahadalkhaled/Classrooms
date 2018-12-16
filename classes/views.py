from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Classroom, Student
from .forms import ClassroomForm, SignUpForm, SignInForm, AddStudent
from django.contrib.auth import login, authenticate, logout

def classroom_list(request):
    classrooms = Classroom.objects.all()
    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    student = Student.objects.filter(classroom=classroom)

    context = {
        "classroom": classroom,
        "student":student
    }
    return render(request, 'classroom_detail.html', context)


def classroom_create(request):
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')

def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)
            
def signout(request):
    logout(request)
    return redirect("signin-form")


def add_student(request):
    form = AddStudent()
    # student = Classroom.objects.get(id=classroom_id)
    if request.method == "POST":
        form = AddStudent(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'add_student.html', context)


def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    
    form = AddStudent(instance=student)
    if request.method == "POST":
        form = AddStudent(request.POST, request.FILES or None, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "student": student,

    }
    return render(request, 'update_student.html', context)



def student_delete(request, student_id):
    student = Student.objects.get(id=student_id)
    classroom = student.classroom
    student.delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-detail', classroom_id=classroom.id)

def confirm_delete(request, student_id):
    
    delete = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        delete_url = delete.classroom.get_absolute_url()
        delete.delete()
        messages.success(request, "Successfully Deleted!")
    
        return HttpResponseRedirect(delete_url)

   
    context = {
        "delete":delete

    }

    return render(request, "delete_student.html", context)











