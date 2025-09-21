from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser


@receiver(pre_save, sender=CustomUser)
def send_activation_email(sender, instance, **kwargs):
    if not instance.pk:
        # مستخدم جديد لم يتم حفظه بعد
        return
    try:
        previous = CustomUser.objects.get(pk=instance.pk)
    except CustomUser.DoesNotExist:
        return
    if previous.is_active == False and instance.is_active == True:
        # تم تفعيل المستخدم الآن
        send_mail(
            subject="تهانينا! تم تفعيل حسابك في منصة مداد بنجاح ✅",
            message=(
                f"السادة/ {instance.first_name} {instance.last_name}\n"
                f"تحية طيبة وبعد،\n\n"
                
                f"يسعدنا إعلامكم أنه تم تفعيل حسابكم في منصة مداد بنجاح.\n\n"
                
                f"🔐 معلومات حسابكم:\n"
                f"• الاسم الكامل: {instance.first_name} {instance.last_name}\n"
                f"• البريد الإلكتروني: {instance.email}\n"
                f"• رقم الهاتف: {instance.phone or 'لم يتم提供'}\n"
                f"• المستوى التعليمي: {instance.get_education_level_display() or 'لم يتم提供'}\n"
                f"• الدور: {instance.get_role_display() or 'لم يتم提供'}\n\n"
                
                f"📋 الخطوات التالية:\n"
                f"1. قم بتسجيل الدخول إلى المنصة\n"
                f"2. استكشف الخدمات والميزات المتاحة\n\n"
                
                # f"🌐 رابط التسجيل:\n"
                # f"http://yourdomain.com/login\n\n"
                
                f"🛡️ نصائح أمنية:\n"
                f"• لا تشارك بيانات الدخول مع أي شخص\n"
                f"• تأكد من استخدام كلمة مرور قوية\n"
                f"• قم بتسجيل الخروج بعد كل استخدام\n\n"
                
                f"📞 للاستفسارات والدعم:\n"
                f"• البريد: medaad.center@gmail.com\n"
                f"• الهاتف: +966554408802\n\n"
                
                f"نشكركم لثقتكم بمنصة مداد، ونتطلع لتقديم أفضل الخدمات لكم.\n\n"
                f"مع أطيب التمنيات،\n"
                f"فريق الدعم الفني - منصة مداد\n"
                f"📍 المملكة العربية السعودية\n"
                f"📧 medaad.center@gmail.com\n"
                # f"🌐 www.yourdomain.com"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
