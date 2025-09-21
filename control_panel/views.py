from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from takwin.models import UserTakwin
from committees.models import UserCommittee


@login_required(login_url="/auth")
def control_panel(request):
    # البرامج المضافة من اللجان
    user_committees = UserCommittee.objects.filter(user=request.user, is_added=True).select_related("committee")
    return render(request, "control_panel.html", {
        "user_committees": user_committees,
    })
