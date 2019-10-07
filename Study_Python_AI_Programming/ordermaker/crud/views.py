from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Message
from .forms import MessageForm
# Create your views here.


def index(request):
    d = {
        'messages': Message.objects.all(),
    }
    return render(request, 'crud/index.html', d)


def add(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        Message.objects.create(**form.cleaned_data)
        return redirect('crud:index')

    d = {
        'form': form,
    }
    return render(request, 'crud/edit.html', d)


def edit(request, editing_id):
    message = get_object_or_404(Message, id=editing_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message.message = form.cleaned_data['message']
            message.save()
            return redirect('crud:index')
    else:
        form = MessageForm({'message': message.message})
    d = {
        'form': form,
    }
    return render(request, 'crud/edit.html', d)


@require_POST
def delete(request):
    delete_ids = request.POST.getlist('delete_ids')
    if delete_ids:
        Message.objects.filter(id__in=delete_ids).delete()
    return redirect('crud:index')
