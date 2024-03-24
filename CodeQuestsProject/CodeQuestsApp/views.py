import subprocess
import time
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import *

# Create your views here.


def index(request):
    context = {
        'user': request.user
    }
    return render(request, 'index.html', context)


def registration(request):
    User = get_user_model()
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST['name']
        surname = request.POST['surname']
        date_of_birth = request.POST['date_of_birth']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect('registration')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
                return redirect('registration')

            else:
                user = User.objects.create_user(username=username, email=email, password=password, name=name,
                                                surname=surname, date_of_birth=date_of_birth)
                user.is_active = True
                user.save()
                return redirect('index')

        else:
            messages.info(request, "Password not the same")
            return redirect('registration')
    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == "POST":

        password = request.POST['password']
        email = request.POST['email']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')

        else:
            messages.info(request, "Wrong credentials")
            return render(request, 'index.html')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')


def delete_acc(request):
    User = get_user_model()

    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id=id)
        user.delete()
        auth.logout(request)
        return render(request, 'index.html')

    else:
        return render(request, 'index.html')


def view_courses(request):
    courses = Course.objects.all()

    context = {
        'courses': courses
    }

    return render(request, 'view_courses.html', context)


def attend_course(request, course_id):
    tasks = Task.objects.filter(course_id=course_id)
    solutions = Solution.objects.filter(user=request.user, task__in=tasks)

    solution_tasks = [solution.task for solution in solutions]
    new_tasks = set(tasks) - set(solution_tasks)

    completed_tasks = []
    unfinished_tasks = list(new_tasks)
    for solution in solutions:
        if solution.passed:
            completed_tasks.append(solution.task)
        else:
            unfinished_tasks.append(solution.task)

    # uklanja duplikate
    unfinished_tasks = list(OrderedDict.fromkeys(unfinished_tasks))
    completed_tasks = list(OrderedDict.fromkeys(completed_tasks))

    percentage = (len(completed_tasks)/(len(unfinished_tasks) + len(completed_tasks))) * 100

    context = {
        'tasks': tasks,
        'solutions': solutions,
        'completed_tasks': completed_tasks,
        'unfinished_tasks': unfinished_tasks,
        'percentage': percentage,
    }
    return render(request, 'attend_course.html', context)


def search_tasks(request):
    query = request.GET.get('q')

    if query:
        tasks = Task.objects.filter(name__icontains=query) | Task.objects.filter(text__icontains=query)
    else:
        tasks = Task.objects.all()

    context = {
        'tasks': tasks,
        'query': query
    }

    return render(request, 'search_tasks.html', context)


def choose_task(request):
    pass
    # mozda ne treba cini mi se vidicemo


def solve_task(request, task_id, match_id):
    m_id = match_id

    try:
        match = Match.objects.get(id=match_id)
    except ObjectDoesNotExist:
        match = None

    message = ''
    correct = False
    task = Task.objects.get(id=task_id)
    course = None
    if hasattr(task, 'course'):
        course = task.course

    if request.method == "POST":
        code = request.POST['code']
        command = ['python', '-c', code]
        output = ''
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=5, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = str(e.output)

        if output.strip() == task.correct_output.strip():
            solution = Solution.objects.create(user=request.user, task=task, user_code=code, match=match, output=output)
            solution.save()
            message = 'Your task is completed successfully!'
            correct = True
            if match_id != 0:
                return redirect('/match_result/{}'.format(match.id))

        else:
            message = 'Incorrect output'
            if match_id != 0:
                solution = Solution.objects.create(user=request.user, task=task, user_code=code, match=match,
                                                   output=output)
                solution.save()
                return redirect('/match_result/{}'.format(match.id))

    context = {
        'task': task,
        'message': message,
        'correct': correct,
        'course': course,
        'm_id': m_id,
    }
    return render(request, 'solve_task.html', context)


def check_match_status(request):
    match = Match.objects.filter(first_user=request.user).last()
    if match and match.second_user is not None:
        data = {
            'joined': True
        }
        print('True')
    else:
        data = {
            'joined': False
        }
        print('False')
    return JsonResponse(data)


def join_queue(request):
    # bira vrstu zadatka i prog jezik
    # ceka protivnika

    queued_matches = Match.objects.filter(queued=True).exclude(first_user=request.user)
    matched = False
    for match in queued_matches:
        # ovdje idu svi uslovi za validan mec, pa tek onda ovo sto sam sad stavio
        match.second_user = request.user
        match.queued = False
        match.save()
        matched = True
        break
        # sad vjv trazimo od apija zadatak i saljemo usere u solve_task

    if not matched:
        match = Match.objects.create(first_user=request.user)
        match.save()

    context = {
        'matched': matched,
        'match_id': match.id
    }
    return render(request, 'join_queue.html', context)


def match_result(request, match_id):
    match = Match.objects.get(id=match_id)
    you = None
    opponent = None
    if match.first_user.id == request.user.id:
        you = match.first_user
        opponent = match.second_user
    else:
        you = match.second_user
        opponent = match.first_user

    your_solution = Solution.objects.filter(user=you, match=match).last()
    opponent_solution = Solution.objects.filter(user=opponent, match=match).last()

    context = {
        'you': you,
        'opponent': opponent,
        'your_solution': your_solution,
        'opponent_solution': opponent_solution,
    }

    return render(request, 'match_result.html', context)


def view_profile(request):
    pass


def view_table(request):
    pass


def match_history(request):
    pass




