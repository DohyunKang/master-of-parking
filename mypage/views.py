from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CombinedUserProfileForm
from .models import MypageProfile

@login_required
def mypage(request):
    if not hasattr(request.user, 'mypage_profile'):
        MypageProfile.objects.create(user=request.user)

    profile = request.user.mypage_profile

    if request.method == 'POST':
        form = CombinedUserProfileForm(request.POST, request.FILES, instance=profile, user_instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다!')
            return redirect('mypage:mypage')
        else:
            messages.error(request, '프로필 업데이트에 실패했습니다. 다시 시도해주세요.')
    else:
        form = CombinedUserProfileForm(instance=profile, user_instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'mypage/mypage.html', context)
