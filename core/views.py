from datetime import datetime, timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import OpenHoursUTC, StoreStatus, Report


class TriggerReport(APIView):
        
    def get(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        open_hours_utc = OpenHoursUTC.objects.filter(store_id=store_id)
        store_status = StoreStatus.objects.filter(store_id=store_id)
        utc_time = datetime.now(timezone.utc)
        curr_day = utc_time.weekday()
        curr_hour = utc_time.hour
        curr_min = utc_time.minute
        uptime_last_hour, uptime_last_day, uptime_last_week, downtime_last_hour, downtime_last_day, downtime_last_week = 0, 0, 0, 0, 0, 0
        if not open_hours_utc:
            open = StoreStatus.objects.filter(store_id=store_id, status='active').count()
            close = StoreStatus.objects.filter(store_id=store_id, status='inactive').count()
            if open==0 and close==0:
                uptime_last_hour, uptime_last_day, uptime_last_week, downtime_last_hour, downtime_last_day, downtime_last_week = 30, 12, 84, 30, 12, 84
            elif open==0:
                uptime_last_hour, uptime_last_day, uptime_last_week, downtime_last_hour, downtime_last_day, downtime_last_week = 0, 0, 0, 60, 24, 168
            elif close==0:
                uptime_last_hour, uptime_last_day, uptime_last_week, downtime_last_hour, downtime_last_day, downtime_last_week = 60, 24, 168, 0, 0, 0
            else:
                open_ratio = (open)/(open+close) 
                close_ratio = (close)/(open+close)
                uptime_last_hour, uptime_last_day, uptime_last_week, downtime_last_hour, 
                downtime_last_day, downtime_last_week = 60*open_ratio, 24*open_ratio, 168*open_ratio, 
                60*close_ratio, 24*close_ratio, 168*close_ratio
        
        # hour  and day calculation
        store_open = OpenHoursUTC.objects.filter(store_id=store_id, day=curr_day)
        open = 0
        close = 0
        if store_open:
            for obj in store_status:
                if obj.timestamp_utc.weekday() == utc_time.weekday():
                    if obj.status == 'active':
                        open+=1
                    else:
                        close+=1
        if open==0 and close==0:
            uptime_last_hour, uptime_last_day, downtime_last_hour, downtime_last_day = 30, 12, 30, 12
        elif open==0:
            uptime_last_hour, uptime_last_day, downtime_last_hour, downtime_last_day = 0, 0, 60, 24
        elif close==0:
             uptime_last_hour, uptime_last_day, downtime_last_hour, downtime_last_day = 60, 24, 0, 0
        else:
            open_ratio = (open)/(open+close) 
            close_ratio = (close)/(open+close)
            uptime_last_hour, uptime_last_day, downtime_last_hour, 
            downtime_last_day = 60*open_ratio, 24*open_ratio,60*close_ratio, 24*close_ratio
        
        
        # for week calculation
        open = 0
        close = 0
        for obj in store_status:
            if obj.status == 'active':
                open+=1
            else:
                close+=1
        if open==0 and close==0:
            uptime_last_week, downtime_last_week = 84, 84
        elif open==0:
            uptime_last_week, downtime_last_week = 0, 168
        elif close==0:
            uptime_last_week, downtime_last_week = 168, 0
        else:
            open_ratio = (open)/(open+close) 
            close_ratio = (close)/(open+close)
            uptime_last_week, downtime_last_week = 168*open_ratio, 168*close_ratio
        report = Report.objects.create(uptime_last_hour=uptime_last_hour, 
                                       uptime_last_day=uptime_last_day,              
                                       uptime_last_week=uptime_last_week, 
                                       downtime_last_hour=downtime_last_hour, 
                                       downtime_last_day=downtime_last_day, 
                                       downtime_last_week=downtime_last_week)
        return Response(data=Report.objects.all().count(), status=HTTP_200_OK)             

class GetReport(APIView):

        def get(self, request, *args, **kwargs):
            report_id = request.query_params.get('report_id')
            report = Report.objects.filter(id=report_id).last()
            if report:
                response_data = {}
                response_data["status"] = "complete"
                response_data["uptime_last_hour"] = report.uptime_last_hour
                response_data["uptime_last_day"] = report.uptime_last_day
                response_data["uptime_last_week"] = report.uptime_last_week
                response_data["downtime_last_hour"] = report.downtime_last_hour
                response_data["downtime_last_day"] = report.downtime_last_day
                response_data["uptime_last_week"] = report.uptime_last_week
                return Response(data=response_data, status=HTTP_200_OK)
            return Response(data={"status":"running"}, status=HTTP_200_OK)

