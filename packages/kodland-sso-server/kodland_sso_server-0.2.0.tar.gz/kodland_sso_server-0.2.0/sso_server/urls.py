from django.urls import path
from .views import TokenView, UserDataView, GetStudentInfoView

urlpatterns = [
	path('token', TokenView.as_view(), name='token'),
	path('info', UserDataView.as_view(), name='user_info'),
	path('student_info', GetStudentInfoView.as_view(), name='student_info')
]
