from django.db import models
from django.conf import settings
import os


ASPECT_CHOICES = [
    ('tarbawiu', 'تربوي'),
    ('shareiu', 'شرعي'),
    ('mhari', 'مهاري'),
    ('medad', 'مداد'),
]

from django.conf import settings
import os

class Takwin(models.Model):
    aspect = models.CharField(
        max_length=20,
        choices=ASPECT_CHOICES,
        verbose_name="الجانب"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان التكوين")
    description = models.TextField(verbose_name="وصف التكوين")
    image = models.ImageField(
        upload_to="takwin_images/",
        blank=True,
        null=True,
        verbose_name="صورة"
    )
    link = models.URLField(blank=True, null=True, verbose_name="رابط")
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="pdfs/", blank=True, null=True, verbose_name="ملف pdf")

    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return os.path.join(settings.MEDIA_URL, "takwin_images/medad_logo2.webp")
        # حط صورة default.jpg داخل MEDIA_ROOT/takwin_images/

    class Meta:
        verbose_name = "تكوين"
        verbose_name_plural = "التكوين"

    def __str__(self):
        return self.title


class UserTakwin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_takwins")
    takwin = models.ForeignKey(Takwin, on_delete=models.CASCADE, related_name="user_takwins")
    is_done = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = 'منجز' if self.is_done else 'غير منجز'
        return f"{self.user.email} - {self.takwin.title} ({status})"
