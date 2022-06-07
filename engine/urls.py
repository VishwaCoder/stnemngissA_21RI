from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home),
    path('task1/', views.get_logical_view, name='task1'),
    path('task5/', views.get_query_patterns, name='task5'),
    path('task6/', views.get_inverted_index, name='task6'),
    path('task7/', views.get_suffix_array, name='task7'),
    path('task8/', views.get_brut_force, name='task8'),
    path('task9/', views.get_KMP, name='task9'),
    path('task10/', views.get_BM, name='task10'),
    path('task11/', views.get_Shift_Or, name='task11'),
    path('query_patterns/', views.search_by_query_patterns),
    path('inv_query/', views.search_by_invIndex),
    path('suffix_array/', views.suffix_array_algo),
    path('brut_force/', views.brut_force_algo),
    path('kmp_algo/', views.kmp_algo),
    path('bm_algo/', views.bm_algo),
    path('shift_or_algo/', views.shift_or_algo),
]
