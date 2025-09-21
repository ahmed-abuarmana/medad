from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Ads, Quotes, Suggestions
from django.core.mail import send_mail
from django.conf import settings

@login_required(login_url="/auth")
def index(request):
    ads = Ads.objects.all()
    quote = Quotes.objects.order_by("?").first()
    return render(request, "main/index.html", {
        "ads": ads,
        "quote": quote
    })


def auth(request):
    return render(request, "auth/auth.html")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        education_level = request.POST.get("education_level")
        role = request.POST.get("role")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # التحقق من وجود البريد مسبقاً
        if CustomUser.objects.filter(email=email).exists():
            return render(request, "auth/register.html", {
                "message": "البريد الإلكتروني مسجل مسبقاً",
                "first_name": first_name,
                "last_name": last_name, 
                "email": email,
                "phone": phone, 
                "password": password,
                "password2": password2,
            })
        
        # التحقق من تطابق كلمة المرور
        if password != password2:
            return render(request, "auth/register.html", {
                "message": "كلمتان المرور غير متطابقتين",
                "first_name": first_name,
                "last_name": last_name, 
                "email": email,
                "phone": phone, 
            })

        # إنشاء المستخدم
        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
            education_level=education_level,
            password=password
        )

        # إرسال إيميل للأدمن
        send_mail(
            subject="مستخدم جديد بانتظار التفعيل",
            message=(
                f"تم تسجيل مستخدم جديد:\n\n"
                f"الاسم: {first_name} {last_name}\n"
                f"البريد: {email}\n"
                f"الهاتف: {phone}\n"
                f"المستوى التعليمي: {education_level}\n"
                f"الدور: {role}\n\n"
                f"الرجاء الدخول للوحة التحكم وتفعيل حسابه."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["medaad.center@gmail.com"],  # ضع إيميل الأدمن هنا
            fail_silently=False,
        )

        return render (request, "auth/login.html", {
            "success_message": "تم إنشاء الحساب بنجاح!✅ في انتظار قبول الإدارة لحسابك"
        })

    return render(request, "auth/register.html")



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # البحث عن المستخدم بالبريد الإلكتروني أولاً
            user = CustomUser.objects.get(email=email)
            
            # التحقق من كلمة المرور يدويًا
            if user.check_password(password):
                # الآن تحقق من حالة الحساب
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect("/admin/")
                    else:
                        return redirect("/")
                else:
                    # الحساب موجود ولكن غير نشط
                    return render(request, "auth/login.html", {
                        "error_message": "حساب المستخدم غير فعال. يرجى الانتظار حتى يصلك إيميل تفعيل الحساب",
                        "email": email,
                    })
            else:
                # كلمة المرور خاطئة
                raise CustomUser.DoesNotExist()
                
        except CustomUser.DoesNotExist:
            # المستخدم غير موجود أو كلمة المرور خاطئة
            return render(request, "auth/login.html", {
                "error_message": "البريد الإلكتروني غير صحيح أو كلمة المرور غير صحيحة",
                "email": email,
            })

    return render(request, "auth/login.html")


@login_required(login_url="/auth")
def edit_profile(request):
    user = request.user  # المستخدم الحالي

    if request.method == "POST":
        # جلب البيانات من الفورم
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        education_level = request.POST.get("education_level")
        role = request.POST.get("role")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # التحقق من البريد الإلكتروني (إذا تم تغييره)
        if email != user.email and CustomUser.objects.filter(email=email).exists():
            return render(request, "auth/profile.html", {
                "user": user,
                "error_message": "هذا البريد الإلكتروني مستخدم بالفعل",
                "ROLE_CHOICES": CustomUser.ROLE_CHOICES,
                "EDUCATION_CHOICES": CustomUser.EDUCATION_CHOICES,
                })

        # تحديث البيانات
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.education_level = education_level
        user.role = role

        # تحديث كلمة المرور إذا كانت موجودة
        if password1 or password2:
            if password1 != password2:
                return render(request, "auth/profile.html", {
                    "user": user,
                    "error_message": "كلمتا المرور غير متطابقتين",
                    "ROLE_CHOICES": CustomUser.ROLE_CHOICES,
                    "EDUCATION_CHOICES": CustomUser.EDUCATION_CHOICES,
                    })
            else:
                user.set_password(password1)

        # حفظ التعديلات
        user.save()
        
        # ملاحظة: إذا غيّر كلمة المرور، لازم يعمل تسجيل دخول من جديد
        if password1:
            return redirect("/login")

        return render(request, "auth/profile.html", {
            "success_message": "تم تحديث بياناتك بنجاح ✅",
            "ROLE_CHOICES": CustomUser.ROLE_CHOICES,
            "EDUCATION_CHOICES": CustomUser.EDUCATION_CHOICES,
        })

    return render(request, "auth/profile.html", {
        "user": user,
        "ROLE_CHOICES": CustomUser.ROLE_CHOICES,
        "EDUCATION_CHOICES": CustomUser.EDUCATION_CHOICES,
    })


@login_required(login_url="/auth")
def logout_view(request):
    logout(request)  # حذف الجلسة
    return render(request, "auth/auth.html")


@login_required
def add_suggestion(request):
    if request.method == "POST":
        # الحصول على المحتوى من الفورم
        content = request.POST.get('content')
        
        # التحقق من وجود المحتوى
        if content:
            # إنشاء المقترح وحفظه في قاعدة البيانات
            suggestion = Suggestions.objects.create(
                content=content,
                user=request.user  # ربط المقترح بالمستخدم الحالي
            )
            return redirect("index")  # إعادة التوجيه للصفحة الرئيسية بعد الحفظ
    
    # في حالة GET أو إذا كان الفورم غير صالح، عرض الصفحة
    return render(request, "main/index.html")



