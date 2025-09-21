from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField
import os

COMMITTEES_CHOICES = [
    ('cultural', 'الثقافية'),
    ('media', 'الإعلامية'),
    ('scientific', 'العلمية'),
    ('social', 'الاجتماعية'),
    ('sports', 'الرياضية'),
    ('volunteer', 'التحفيزية'),
]

EDUCATION_CHOICES = [
    ('ابتدائي', 'ابتدائي'),
    ('متوسط', 'متوسط'),
    ('ثانوي', 'ثانوي'),
    ('جامعي', 'جامعي'),
]

class Committee(models.Model):
    committees = models.CharField(
        max_length=20,
        choices=COMMITTEES_CHOICES,
        verbose_name="اللجنة",
        help_text="اختر اللجنة المناسبة"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان البرنامج")
    description = models.TextField(verbose_name="وصف البرنامج")
    image = models.ImageField(
        upload_to="committees_images/",
        blank=True,
        null=True,
        verbose_name="صورة"
    )
    link = models.URLField(blank=True, null=True, verbose_name="رابط")
    education_levels = MultiSelectField(
        choices=EDUCATION_CHOICES,
        max_length=100,
        verbose_name="المرحلة الإشرافية"
    )
    pdf = models.FileField(upload_to='committees/', blank=True, null=True, verbose_name="ملف pdf")

    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return os.path.join(settings.MEDIA_URL, "committees_images/medad_logo2.webp")

    class Meta:
        verbose_name = 'اللجنة'
        verbose_name_plural = 'اللجان'

    def __str__(self):
        return f"{self.title} ({self.get_committees_display()})"



class UserCommittee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_committees")
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name="user_committees")
    is_added = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'committee'], name='unique_user_committee')
        ]

    def __str__(self):
        status = 'تم إضافته' if self.is_added else 'لم يتم إضافته'
        return f"{self.user.email} - {self.committee.title} ({status})"
