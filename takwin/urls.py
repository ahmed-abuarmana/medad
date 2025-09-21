from django.urls import path
from . import views

urlpatterns = [
    path('', views.takwin, name="takwin"),   # الصفحة الرئيسية للتكوين
    path('tarbawiu/', views.tarbawiu, name="tarbawiu"),
    path('shareiu/', views.shareiu, name="shareiu"),
    path('mhari/', views.mhari, name="mhari"),
    path('medad/', views.medad, name="medad"),
    path('toggle_takwin/<int:takwin_id>/', views.toggle_takwin, name='toggle_takwin'),
    path('pdf/<int:takwin_id>/', views.pdf_view, name='pdf_view'),
]
