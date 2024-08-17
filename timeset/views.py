from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TimeSet
from .forms import TimeSetForm

@login_required
def set_time(request):
    if request.method == 'POST':
        form = TimeSetForm(request.POST)
        if form.is_valid():
            weekday = form.cleaned_data['weekday']
            entry_time = form.cleaned_data['entry_time']
            exit_time = form.cleaned_data['exit_time']

            if entry_time and exit_time:  # Ensure both times are provided
                timeset, created = TimeSet.objects.get_or_create(user=request.user, weekday=weekday)
                timeset.entry_time = entry_time
                timeset.exit_time = exit_time
                timeset.save()

                return redirect('time_set:set_time')
            else:
                form.add_error(None, "입차 시간과 출차 시간을 모두 입력해야 합니다.")
    else:
        form = TimeSetForm()

    times = TimeSet.objects.filter(user=request.user)
    context = {
        'form': form,
        'times': times,
    }
    return render(request, 'timeset/timeset_form.html', context)

@login_required
def reset_times(request):
    TimeSet.objects.filter(user=request.user).delete()
    return redirect('time_set:set_time')
