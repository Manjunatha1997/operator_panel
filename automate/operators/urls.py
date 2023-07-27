from django.urls import URLPattern, path,re_path
from operators import views

urlpatterns = [
    # re_path(r'^inspection/start_process/$', views.start_process_view),
    # re_path(r'^inspection/end_process/$', views.end_process_view),
    # re_path(r'^inspection/getDefectList/(?P<inspection_id>[A-Za-z0-9-_]+)', views.get_metrics_view),
    # re_path(r'^inspection/get_running_process/$', views.get_running_process_view),
    # re_path(r'^parts/get_all_parts/$', views.get_all_parts_view),
    # re_path(r'^reports/getMegaReport/$', views.get_mega_report_view),

    
    re_path(r'^start_process/$', views.start_process_view),
    re_path(r'^end_process/$', views.end_process_view),
    re_path(r'^get_metrics/(?P<inspection_id>[A-Za-z0-9-_]+)', views.get_metrics_view),
    re_path(r'^get_running_process/$', views.get_running_process_view),
    re_path(r'^get_all_parts/$', views.get_all_parts_view),
    re_path(r'^get_mega_report/$', views.get_mega_report_view),

    re_path(r'^start_inspection/$', views.start_inspection_view),
    re_path(r'get_redis_image/(?P<key>[A-Za-z0-9-_]+)/$', views.get_redis_image),
    re_path(r'set_confidence/$', views.set_confidence),


    # this below url is going to be called from worker script with all the details as payload
    re_path(r'^save_inspection_details/$', views.save_inspection_details_view),
]
