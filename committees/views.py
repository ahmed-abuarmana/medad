from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Committee, UserCommittee
from django.shortcuts import get_object_or_404, redirect

@login_required(login_url="/auth")
def committees(request):
    return render(request, "index.html")


@login_required(login_url="/auth")
def social(request):
    committees = Committee.objects.filter(committees='social').order_by('-id')

    for c in committees:
        user_committee = UserCommittee.objects.filter(user=request.user, committee=c).first()
        c.is_added = user_committee.is_added if user_committee else False

    return render(request, 'social.html', {
        'committees': committees,
    })


@login_required(login_url="/auth")
def media(request):
    committees = Committee.objects.filter(committees='media').order_by('-id')

    for c in committees:
        user_committee = UserCommittee.objects.filter(user=request.user, committee=c).first()
        c.is_added = user_committee.is_added if user_committee else False

    return render(request, 'media.html', {
        'committees': committees,
    })


@login_required(login_url="/auth")
def cultural(request):
    committees = Committee.objects.filter(committees='cultural').order_by('-id')

    for c in committees:
        user_committee = UserCommittee.objects.filter(user=request.user, committee=c).first()
        c.is_added = user_committee.is_added if user_committee else False

    return render(request, 'cultural.html', {
        'committees': committees,
    })


@login_required(login_url="/auth")
def scientific(request):
    committees = Committee.objects.filter(committees='scientific').order_by('-id')

    for c in committees:
        user_committee = UserCommittee.objects.filter(user=request.user, committee=c).first()
        c.is_added = user_committee.is_added if user_committee else False

    return render(request, 'scientific.html', {
        'committees': committees,
    })


@login_required(login_url="/auth")
def sports(request):
    committees = Committee.objects.filter(committees='sports').order_by('-id')

    for c in committees:
        user_committee = UserCommittee.objects.filter(user=request.user, committee=c).first()
        c.is_added = user_committee.is_added if user_committee else False

    return render(request, 'sports.html', {
        'committees': committees,
    })


@login_required(login_url="/auth")
def volunteer(request):
    committees = Committee.objects.filter(committees='volunteer').order_by('-id')

    for c in committees:
        user_committee = UserCommittee.objects.filter(user=request.user, committee=c).first()
        c.is_added = user_committee.is_added if user_committee else False

    return render(request, 'volunteer.html', {
        'committees': committees,
    })


@login_required(login_url="/auth")
def toggle_committee(request, committee_id):
    committee = get_object_or_404(Committee, id=committee_id)

    user_committee, created = UserCommittee.objects.get_or_create(
        user=request.user,
        committee=committee,
        defaults={'is_added': True}
    )

    if not created:
        # لو كان موجود، غير الحالة
        user_committee.is_added = not user_committee.is_added
        user_committee.save()

    # ارجع المستخدم لنفس الصفحة
    return redirect(request.META.get('HTTP_REFERER', 'social'))