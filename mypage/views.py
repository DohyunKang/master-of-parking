from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm

@login_required
def mypage(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '당신의 프로필이 성공적으로 업데이트 되었습니다!')
            return redirect('mypage:mypage')
        else:
            messages.error(request, '프로필 업데이트에 실패했습니다. 다시 시도해주세요.')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'mypage/mypage.html', {'form': form})
