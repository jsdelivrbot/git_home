import logging
import datetime
import math

from Core.models import *
from Core.mail import Mail


class Query(object):

    logger = logging.getLogger(__name__)
        
    def overview_year(self, user, year):
        months = []
    
        for month in range(1,13):
            if month == 12:
                allAcquisitions = Acquisition.objects.all().filter(user=user, end__range=(datetime.datetime(year, month, 1), datetime.datetime(year+1, 1, 1))).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
            else:
                allAcquisitions = Acquisition.objects.all().filter(user=user, end__range=(datetime.datetime(year, month, 1), datetime.datetime(year, month+1, 1))).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
            
            min_month = float(0)  
            
            for entry in allAcquisitions:
                min_month = min_month + (entry.end.hour - entry.start.hour) * 60 + entry.end.minute - entry.start.minute
            months.append([month, float("%.2f" % (min_month/60))])
        
        return months
    
    def overview_month(self, user, month, year):
        days = []
        
        d1 = datetime.datetime(year, month, 1).day
        if(month < 12):
            d2 = (datetime.datetime(year, month+1, 1) - datetime.timedelta(days=1)).day + 1
        else:
            d2 = (datetime.datetime(year+1, 1, 1) - datetime.timedelta(days=1)).day + 1
        
        for day in range(d1, d2):
        #for day in range(1,28):
            allAcquisitions = Acquisition.objects.all().filter(user=user, end__range=(datetime.datetime(year, month, day), datetime.datetime(year, month, day)+datetime.timedelta(days=1))).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
            
            min_day = float(0)  
            
            for entry in allAcquisitions:
                min_day = min_day + (entry.end.hour - entry.start.hour) * 60 + entry.end.minute - entry.start.minute
            days.append([day, float("%.2f" % (min_day/60))])
            
        return days
    
    def overview_week(self, user, today):
        days = []
        
        i = 0
        while (datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(days=i)).isoweekday() != 7:
            i = i + 1
            
        d1 = (datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(days=i))
        
        for day in range(1, 8):     # Achtung!!!
            allAcquisitions = Acquisition.objects.all().filter(user=user, end__range=(d1 + datetime.timedelta(days=day), d1 + datetime.timedelta(days=day+1))).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
            
            min_day = float(0)
            
            for entry in allAcquisitions:
                min_day = min_day + (entry.end.hour - entry.start.hour) * 60 + entry.end.minute - entry.start.minute
            
            #days.append([(d1 + datetime.timedelta(days=day)).strftime("%a"), float("%.2f" % (min_day/60))])
            days.append(str(float("%.2f" % (min_day/60))))
        
        return days
    
    def overview_day(self, user, today):
        allAcquisitions = Acquisition.objects.all().filter(user=user, end__range=(today, today+datetime.timedelta(days=1))).order_by("end").exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
        
        start = datetime.time(23, 59)
        end = datetime.time(0, 0)
        end_last = datetime.time(0, 0)
        minutes = 0
        
        projects = []
        
        for ac in allAcquisitions:
            if end_last == datetime.time(0, 0):
                end_last = datetime.time(ac.start.hour, ac.start.minute)
            if end_last < datetime.time(ac.start.hour, ac.start.minute):
                minutes = minutes + ac.start.hour*60 + ac.start.minute - (end_last.hour*60 + end_last.minute )
            if start > datetime.time(ac.start.hour, ac.start.minute):
                start = datetime.time(ac.start.hour, ac.start.minute)
            if end < datetime.time(ac.end.hour, ac.end.minute):
                end = datetime.time(ac.end.hour, ac.end.minute)
                end_last = datetime.time(ac.end.hour, ac.end.minute)
            
            if ac.project not in projects:
                projects.append(ac.project)
                
        for project in projects:
            allProjectAcquisitions = Acquisition.objects.all().filter(user=user, end__range=(today, today+datetime.timedelta(days=1)), project = project).order_by("end")
            sum = float(0)
            for ac in allProjectAcquisitions:
                sum = sum + (ac.end - ac.start).seconds / 60 
            project.sum = str(float("%.2f" % (sum/60)))
            
        delta = datetime.timedelta(minutes=minutes)
        breakhours = math.floor(delta.days*24+delta.seconds/3600.0)
        breakstring = str(int(breakhours))+':'+str(int(minutes - breakhours*60))
        
        entire = end.hour*60 + end.minute - (start.hour*60 + start.minute) - minutes
        entirehours = math.floor(entire/60)
        entirestring = str(int(entirehours))+':'+str(int(entire - entirehours*60))
            
        return {'projects':projects, 'breakstring':breakstring, 'entirestring':entirestring, 'start':start, 'end':end, 'allAcquisitions':allAcquisitions }
    
    def analysis_violation(self, user):
        
        class DayClass:
            start = ""
            end = ""
            day = ""
            minutes = ""
            pause = ""

        for violation in Violation.objects.filter(user = user):
            violation.delete()
        
        allAcquisitions = Acquisition.objects.all().filter(user=user).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
        
        dates = []
        entries = []
        
        for ac in allAcquisitions:
            if ac.start.date() not in dates:
                dates.append(ac.start.date())
        
        #entries.append(DayClass(start, end, minutes, pause))
        
        for date in dates:
            acquisitions = Acquisition.objects.all().filter(user=user, end__range=(date, date+datetime.timedelta(days=1))).order_by("end")
            
            start = datetime.time(23, 59)
            end = datetime.time(0, 0)
            end_last = datetime.time(0, 0)
            minutes = 0
            
            for ac in acquisitions:
                if end_last == datetime.time(0, 0):
                    end_last = datetime.time(ac.start.hour, ac.start.minute)
                if end_last < datetime.time(ac.start.hour, ac.start.minute):
                    minutes = minutes + ac.start.hour*60 + ac.start.minute - (end_last.hour*60 + end_last.minute )
                if start > datetime.time(ac.start.hour, ac.start.minute):
                    start = datetime.time(ac.start.hour, ac.start.minute)
                if end < datetime.time(ac.end.hour, ac.end.minute):
                    end = datetime.time(ac.end.hour, ac.end.minute)
                    end_last = datetime.time(ac.end.hour, ac.end.minute)
                    
            day = DayClass()
            day.start = start
            day.end = end
            day.day = date
            day.minutes = end.hour*60 + end.minute - (start.hour*60 + start.minute) - minutes
            day.pause = minutes
            entries.append(day)
            #entries.append(DayClass(start, end, end.hour*60 + end.minute - (start.hour*60 + start.minute) - minutes, minutes))
            
        for entry in entries:
            if entry.minutes-entry.pause >= 360 and entry.minutes-entry.pause < 540:
                if entry.pause < 45:
                    Violation(user = user, start = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.start.hour, entry.start.minute), end = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.end.hour, entry.end.minute), pause = entry.pause, type = 0).save()
                    Mail().mail_violation(user, str(entry.day.year) + '-' + str(entry.day.month) + '-' + str(entry.day.day) + ': < 30 minutes pause')
            if entry.minutes-entry.pause >= 540:
                if entry.pause < 45:
                    Violation(user = user, start = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.start.hour, entry.start.minute), end = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.end.hour, entry.end.minute), pause = entry.pause, type = 0).save()
                    Mail().mail_violation(user, str(entry.day.year) + '-' + str(entry.day.month) + '-' + str(entry.day.day) + ': < 45 minutes pause')
            if entry.minutes-entry.pause > 600:
                Violation(user = user, start = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.start.hour, entry.start.minute), end = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.end.hour, entry.end.minute), pause = entry.pause, type = 1).save()
                Mail().mail_violation(user, str(entry.day.year) + '-' + str(entry.day.month) + '-' + str(entry.day.day) + ': > 10 hours work')
            #if day before
                #Violation(user = user, start = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.start.hour, entry.start.minute), end = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.end.hour, entry.end.minute), pause = entry.pause, type = 2).save()
            #if week
                #Violation(user = user, start = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.start.hour, entry.start.minute), end = datetime.datetime(entry.day.year, entry.day.month, entry.day.day, entry.end.hour, entry.end.minute), pause = entry.pause, type = 3).save()
        return 1

    def average_hours(self, user, year):
        allAcquisitions = Acquisition.objects.all().filter(user=user, end__range=(datetime.datetime(year, 1, 1), datetime.datetime(year+1, 1, 1))).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
        minutes = 0
        days = []

        for entry in allAcquisitions:
            minutes = minutes + (entry.end.hour - entry.start.hour) * 60 + entry.end.minute - entry.start.minute
            if entry.start.date() not in days:
                days.append(entry.start.date())

        if len(days) > 0:
            return minutes/len(days)
        else:
            return 0
