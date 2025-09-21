from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Takwin, UserTakwin
from django.shortcuts import redirect, get_object_or_404


@login_required(login_url="/auth")
def takwin(request):

    def calc_percentage(done, total):
        return round((done / total) * 100) if total > 0 else 0

    num_tarbawiu = Takwin.objects.filter(aspect='tarbawiu').order_by('-created_at').count()
    num_done_tarbawiu = UserTakwin.objects.filter(user=request.user, takwin__aspect='tarbawiu', is_done=True).count()
    progress_tarbawiu = calc_percentage(num_done_tarbawiu, num_tarbawiu)
    
    num_shareiu = Takwin.objects.filter(aspect='shareiu').order_by('-created_at').count()
    num_done_shareiu = UserTakwin.objects.filter(user=request.user, takwin__aspect='shareiu', is_done=True).count()
    progress_shareiu = calc_percentage(num_done_shareiu, num_shareiu)

    num_mhari = Takwin.objects.filter(aspect='mhari').order_by('-created_at').count()
    num_done_mhari = UserTakwin.objects.filter(user=request.user, takwin__aspect='mhari', is_done=True).count()
    progress_mhari = calc_percentage(num_done_mhari, num_mhari)

    num_medad = Takwin.objects.filter(aspect='medad').order_by('-created_at').count()
    num_done_medad = UserTakwin.objects.filter(user=request.user, takwin__aspect='medad', is_done=True).count()
    progress_medad = calc_percentage(num_done_medad, num_medad)

    num_takwins = num_tarbawiu + num_shareiu + num_mhari + num_medad
    num_done_takwins = num_done_tarbawiu + num_done_shareiu + num_done_mhari + num_done_medad
    progress_takwins = calc_percentage(num_done_takwins, num_takwins)


    return render(request, 'takwin.html', {
        "num_takwins": num_takwins, "num_done_takwins": num_done_takwins, "progress_takwins": progress_takwins,
        "num_tarbawiu": num_tarbawiu, "num_done_tarbawiu": num_done_tarbawiu, "progress_tarbawiu": progress_tarbawiu,
        "num_shareiu": num_shareiu, "num_done_shareiu": num_done_shareiu, "progress_shareiu": progress_shareiu,
        "num_mhari": num_mhari, "num_done_mhari": num_done_mhari, "progress_mhari": progress_mhari,
        "num_medad": num_medad, "num_done_medad": num_done_medad, "progress_medad": progress_medad,
    })


@login_required(login_url="/auth")
def tarbawiu(request):
    takwin_list = Takwin.objects.filter(aspect='tarbawiu').order_by('-created_at')

    for t in takwin_list:
        user_takwin = UserTakwin.objects.filter(user=request.user, takwin=t).first()
        t.is_done = user_takwin.is_done if user_takwin else False

    return render(request, 'tarbawiu.html', {
        'takwin_list': takwin_list,
    })


@login_required(login_url="/auth")
def shareiu(request):
    takwin_list = Takwin.objects.filter(aspect='shareiu').order_by('-created_at')

    for t in takwin_list:
        user_takwin = UserTakwin.objects.filter(user=request.user, takwin=t).first()
        t.is_done = user_takwin.is_done if user_takwin else False

    return render(request, 'shareiu.html', {
        'takwin_list': takwin_list,
    })


@login_required(login_url="/auth")
def mhari(request):
    takwin_list = Takwin.objects.filter(aspect='mhari').order_by('-created_at')

    for t in takwin_list:
        user_takwin = UserTakwin.objects.filter(user=request.user, takwin=t).first()
        t.is_done = user_takwin.is_done if user_takwin else False

    return render(request, 'mhari.html', {
        'takwin_list': takwin_list,
    })


@login_required(login_url="/auth")
def medad(request):
    takwin_list = Takwin.objects.filter(aspect='medad').order_by('-created_at')

    for t in takwin_list:
        user_takwin = UserTakwin.objects.filter(user=request.user, takwin=t).first()
        t.is_done = user_takwin.is_done if user_takwin else False

    return render(request, 'medad.html', {
        'takwin_list': takwin_list,
    })



@login_required(login_url="/auth")
def toggle_takwin(request, takwin_id):
    takwin = get_object_or_404(Takwin, id=takwin_id)

    user_takwin, created = UserTakwin.objects.get_or_create(
        user=request.user,
        takwin=takwin,
        defaults={'is_done': True}
    )

    if not created:
        # لو كان موجود، غير الحالة
        user_takwin.is_done = not user_takwin.is_done
        user_takwin.save()

    # رجّع المستخدم للصفحة السابقة أو للصفحة الرئيسية إذا لم يكن هناك Referer
    return redirect(request.META.get('HTTP_REFERER', '/'))



def pdf_view(request, takwin_id):
    takwin = get_object_or_404(Takwin, id=takwin_id)
    return render(request, 'documents/pdf_view.html', {'takwin': takwin})