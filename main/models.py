from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _

# مدير المستخدمين المخصص
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, role, education_level, password=None, **extra_fields):
        if not email:
            raise ValueError("يجب إدخال البريد الإلكتروني")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
            education_level=education_level,
            **extra_fields
        )
        user.set_password(password)  # تشفير كلمة المرور
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='Admin',
            education_level='جامعي',
            password=password,
            **extra_fields
        )


# نموذج المستخدم المخصص
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # الحقول الخاصة بك
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = [
        ('عضو فريق', 'عضو فريق'),
        ('قائد فريق', 'قائد فريق'),
    ]

    EDUCATION_CHOICES = [
        ('ابتدائي', 'ابتدائي'),
        ('متوسط', 'متوسط'),
        ('ثانوي', 'ثانوي'),
        ('جامعي', 'جامعي'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True, null=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # تضارب الحقول الافتراضية يتم حله هنا
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # بدل user_set الافتراضي
        blank=True,
        help_text="المجموعات التي ينتمي إليها المستخدم",
        verbose_name="groups"
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # بدل user_set الافتراضي
        blank=True,
        help_text="أذونات المستخدم الفردية",
        verbose_name="user permissions"
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        verbose_name = 'مستخدم' 
        verbose_name_plural = 'المستخدمين' 

    def __str__(self):
        return self.email


class Ads(models.Model):
    DAYS = [
        ('السبت', 'السبت'),
        ('الأحد', 'الأحد'),
        ('الإثنين', 'الإثنين'),
        ('الثلاثاء', 'الثلاثاء'),
        ('الأربعاء', 'الأربعاء'),
        ('الخميس', 'الخميس'),
        ('الجمعة', 'الجمعة'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان الإعلان")
    date = models.DateField(verbose_name="التاريخ")
    time = models.TimeField(verbose_name="الوقت")
    place = models.CharField(max_length=200, verbose_name="المكان")
    day = models.CharField(max_length=10, choices=DAYS, verbose_name="اليوم")
    details = models.CharField(max_length=300, help_text="وصف الاعلان")
    more_details = models.CharField(help_text="بإمكانك إدخال رابط هنا فقط", blank=True)
    loacation = models.CharField(verbose_name="الموقع", blank=True, null=True)
    
    class Meta:
        verbose_name = 'إعلان' 
        verbose_name_plural = 'الإعلانات' 
    def __str__(self):
        return self.title


class Quotes(models.Model):
    content = models.CharField(verbose_name="المقولة")

    class Meta:
        verbose_name = 'مقولة' 
        verbose_name_plural = 'مقولات' 

    def __str__(self):
        return self.content


class Suggestions(models.Model):
    content = models.CharField(max_length=255, verbose_name="المقترح")
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="suggestions",
        verbose_name="المستخدم"
    )

    class Meta:
        verbose_name = 'مقترح'
        verbose_name_plural = 'المقترحات'

    def __str__(self):
        return f"{self.content} - {self.user.email}"

    @property
    def user_email(self):
        return self.user.email

    @property
    def user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
