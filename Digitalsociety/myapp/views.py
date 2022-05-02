from cmath import phase
import email
from email import message
import imp
from multiprocessing import context
from os import stat
import pstats
from django.shortcuts import *
from django.http import HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    if "c_email" in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        if uid.role=="Chairman":
            cid=Chairman.objects.get(user_id=uid)
            all_member=Societymember.objects.all()
            context={
                "uid":uid,
                "cid":cid,   
                "all_member":all_member,                    
            }
            return render(request,"myapp/index.html",context)
        elif uid.role=="Member":
            cid = Societymember.objects.get(email=uid)
            all_member=Societymember.objects.all()
            context={
                "uid":uid,   
                "all_member":all_member, 
                "cid":cid,     
            }
            return render(request,"myapp/index.html",context)
        elif uid.role=="watchman":
            cid = Watchman.objects.get(user_id=uid)
            all_member=Societymember.objects.all()
            context={
                "uid":uid,   
                "all_member":all_member, 
                "cid":cid,     
            }
            return render(request,"myapp/index.html",context)
    else:
        return render(request,"myapp/login.html")

def login(request):
    if "c_email" in request.session:
        return redirect("home")
    else:
        if request.POST:
            role=request.POST['role']
            email=request.POST['email']
            password=request.POST['password']
            uid= User.objects.get(email=email)
            if role =="Chairman" and uid.password==password:
                cid = Chairman.objects.get(user_id=uid)
                request.session['c_email']=uid.email
                context={
                    "uid":uid,
                    "cid":cid,
                }
                return render(request,"myapp/index.html", context)
            elif role =="societymember" and uid.password==password:
                cid = Societymember.objects.get(email=uid)
                request.session['c_email']=uid.email
                context={
                    "uid":uid,
                    "cid":cid,
                }
                return render(request,"myapp/index.html", context)
            elif role =="watchman" and uid.password==password:
                cid = Watchman.objects.get(user_id=uid)
                request.session['c_email']=uid.email
                context={
                    "uid":uid,
                    "cid":cid,
                }
                return render(request,"myapp/index.html", context)
            else:
                return render(request,"myapp/login.html")
        else:
                return render(request,"myapp/login.html")
    

def change_password(request):
    uid=User.objects.get(email=request.session['c_email'])
    if request.POST:
        if uid.password == request.POST['oldpassword']:
            newpassword=request.POST['newpassword']
            confirmpassword=request.POST['confirmpassword']
            if newpassword==confirmpassword:
                uid.password=confirmpassword
                uid.save()
                return render(request,'myapp/login.html')
        else:
            return render(request,'myapp/change-password.html')
    else:
            context={
                "uid":uid,
            }
            return render(request,"myapp/change-password.html",context)


def logout(request):
    if "c_email" in request.session:
        del request.session["c_email"]
        return redirect("login")
    else:
        return redirect("login")

def profile(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid=Chairman.objects.get(user_id=uid)
        if request.POST:
            cid.pic=request.FILES['pic']     
            cid.name=request.POST['name']
            cid.contact_no=request.POST['contact_no']
            cid.house_no=request.POST['house_no']
            cid.vehicle_type=request.POST['vehicle_type']
            cid.vehicle_details=request.POST['vehicle_details']
            cid.full_address=request.POST['full_address']
            cid.save()
            return redirect('profile')
        else:
            context={
                "uid":uid,
                "cid":cid,
            }
            return render(request,"myapp/profile.html",context)
    elif uid.role=="Member":
        cid=Societymember.objects.get(email=uid)
        if request.POST:
            cid.pic=request.FILES['pic']     
            cid.name=request.POST['name']
            cid.contact_no=request.POST['contact_no']
            cid.house_no=request.POST['house_no']
            cid.vehicle_type=request.POST['vehicle_type']
            cid.vehicle_details=request.POST['vehicle_details']
            cid.full_address=request.POST['full_address']
            cid.save()
            return redirect('profile')
        else:
            context={
                "uid":uid,
                "cid":cid,
            }
            return render(request,"myapp/profile.html",context)
    elif uid.role=="watchman":
        cid=Watchman.objects.get(user_id=uid)
        if request.POST:
            cid.pic=request.FILES['pic']     
            cid.name=request.POST['name']
            cid.contact_no=request.POST['contact_no']
            cid.email=request.POST['email']
            cid.age=request.POST['age']
            cid.full_address=request.POST['full_address']
            cid.save()
            return redirect('profile')
        else:
            context={
                "uid":uid,
                "cid":cid,
            }
            return render(request,"myapp/profile.html",context)

def add_member(request):
    if "c_email" in request.session:
        if request.POST:
            uid = User.objects.get(email=request.session['c_email'])
            cid= Chairman.objects.get(user_id=uid)
            name=request.POST['name']
            email= request.POST['email']
            contact_no=request.POST['contact_no']
            house_no=request.POST['house_no']
            full_address=request.POST['full_address']
            job_profession=request.POST['job_profession']
            job_address=request.POST['job_address']
            vehicle_type=request.POST['vehicle_type']
            vehicle_details=request.POST['vehicle_details']
            pic =request.FILES['pic']
            oid= Societymember.objects.create(user_id=uid,chairman_id=cid,name=name,email=email,contact_no=contact_no,house_no=house_no,full_address=full_address,job_address=job_address,job_profession=job_profession,vehicle_type=vehicle_type,vehicle_details=vehicle_details,pic=pic)
            mid= User.objects.create(email=email,password="123456",role="Member")
            return redirect('view-member')
        else:
            uid = User.objects.get(email=request.session['c_email'])
            cid = Chairman.objects.get(user_id=uid)
            context={
                'uid':uid,
                'cid':cid,
            }
            return render(request,"myapp/add-member.html",context)
    else:
         return render(request,"myapp/login.html")

def view_member(request):
    if "c_email" in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        if uid.role=="Chairman":
            cid=Chairman.objects.get(user_id=uid)
            all_member=Societymember.objects.all()
            context={
                'uid':uid,
                'cid':cid,
                'all_member':all_member,
            }
            return render(request,"myapp/view-member.html",context)
        elif uid.role=="Member":
            cid=Societymember.objects.get(email=uid)
            all_member=Societymember.objects.all()
            context={
                'uid':uid,
                'cid':cid,
                'all_member':all_member,
            }
            return render(request,"myapp/view-member.html",context)
        elif uid.role=="watchman":
            cid=Watchman.objects.get(user_id=uid)
            all_member=Societymember.objects.all()
            context={
                'uid':uid,
                'cid':cid,
                'all_member':all_member,
            }
            return render(request,"myapp/view-member.html",context)
    else:
        return render(request,"myapp/login.html")

def m_view_profile(request,pk):
    uid = User.objects.get(email=request.session['c_email'])
    mid= Societymember.objects.get(id=pk)
    context={
            "uid":uid,
            "mid":mid,
        }
    return render(request,"myapp/member-profile.html",context)
  
def m_delete_profile(request,pk): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    mid= Societymember.objects.get(id=pk)
    mid.delete() 
    return redirect("view-member")  

def m_edit_profile(request,pk): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    mid= Societymember.objects.get(id=pk)
    context={
            "uid":uid,
            "cid":cid,
            "mid":mid,
        }
    return render(request,"myapp/edit-member.html",context)
     
def m_update_profile(request): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    pid=Societymember.objects.get(id=request.POST['id'])
    if request.POST:  
        pid.name=request.POST['name']
        pid.email=request.POST['email']
        pid.contact_no=request.POST['contact_no']
        pid.house_no=request.POST['house_no']
        pid.vehicle_type=request.POST['vehicle_type']
        pid.vehicle_details=request.POST['vehicle_details']
        pid.full_address=request.POST['full_address']
        pid.job_profession=request.POST['job_profession']
        pid.job_address=request.POST['job_address']
        # pid.pic=request.FILES['pic'] 
        if 'pic' in request.FILES:
            pid.pic=request.FILES['pic'] 
            pid.save()
        pid.save()
        return redirect("view-member")   

def add_event(request):
    uid = User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    if request.POST:
        event_title=request.POST['event_title']
        event_pic=request.FILES['event_pic']
        event_discription=request.POST['event_discription']
        event_date=request.POST['event_date']
        eid= Events.objects.create(user_id=uid,chairman_id=cid,event_title=event_title,event_pic=event_pic,event_date=event_date,event_discription=event_discription)
        return redirect('view-event')
    else:
        context={
                    'uid':uid,
                    'cid':cid,
                }
        return render(request,"myapp/add-event.html",context)

def view_event(request):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid=Chairman.objects.get(user_id=uid)
        all_event=Events.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_event':all_event,
                    }    
        return render(request,"myapp/view-event.html",context)
    elif uid.role =="Member":
        cid=Societymember.objects.get(email=uid)
        all_event=Events.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_event':all_event,
                    }    
        return render(request,"myapp/view-event.html",context)
    elif uid.role =="watchman":
        cid=Watchman.objects.get(user_id=uid)
        all_event=Events.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_event':all_event,
                    }    
        return render(request,"myapp/view-event.html",context)


def edit_event(request,ek): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    eid= Events.objects.get(id=ek)
    context={
            "uid":uid,
            "cid":cid,
            "eid":eid,
        }
    return render(request,"myapp/edit-event.html",context)

def update_event(request): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    ueid=Events.objects.get(id=request.POST['id'])
    if request.POST:  
        ueid.event_title=request.POST['event_title']
        ueid.event_date=request.POST['event_date']
        ueid.event_discription=request.POST['event_discription']
        ueid.event_pic=request.FILES['event_pic'] 
        ueid.save()
        return redirect("view-event") 

def delete_event(request,ek): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    eid= Events.objects.get(id=ek)
    eid.delete() 
    return redirect("view-event")  

def add_notice(request):
    uid = User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    if request.POST:
        notice_title=request.POST['notice_title']
        notice_discription=request.POST['notice_discription']
        notice_date=request.POST['notice_date']
        nid= Notice.objects.create(user_id=uid,chairman_id=cid,notice_title=notice_title,notice_date=notice_date,notice_discription=notice_discription)
        return redirect('view-notice')
    else:
        context={
                    'uid':uid,
                    'cid':cid,
                }
        return render(request,"myapp/add-notice.html",context)

def view_notice(request):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid= Chairman.objects.get(user_id=uid)
        all_notice=Notice.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_notice':all_notice,
                    }    
        return render(request,"myapp/view-notice.html",context)
    elif uid.role =="Member":
        cid= Societymember.objects.get(email=uid)
        all_notice=Notice.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_notice':all_notice,
                    }    
        return render(request,"myapp/view-notice.html",context)
    elif uid.role =="watchman":
        cid= Watchman.objects.get(user_id=uid)
        all_notice=Notice.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_notice':all_notice,
                    }    
        return render(request,"myapp/view-notice.html",context)

def delete_notice(request,nk): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    nid= Notice.objects.get(id=nk)
    nid.delete() 
    return redirect("view-notice") 

def add_photos(request):
    uid = User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    if request.POST:
        c_pic=request.FILES['c_pic']
        pic_name=request.POST['pic_name']
        # pic_date=request.POST['pic_date']
        pic_id= Photos.objects.create(user_id=uid,chairman_id=cid,c_pic=c_pic,pic_name=pic_name)
        return redirect('view-photos')
    else:
        context={
                    'uid':uid,
                    'cid':cid,
                }
        return render(request,"myapp/add-photos.html",context)
    
def view_photos(request):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid=Chairman.objects.get(user_id=uid)
        all_photos=Photos.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_photos':all_photos,
                    }    
        return render(request,"myapp/view-photos.html",context)
    elif uid.role=="Member":
        cid=Societymember.objects.get(email=uid)
        all_photos=Photos.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_photos':all_photos,
                    }    
        return render(request,"myapp/view-photos.html",context)
    elif uid.role=="watchman":
        cid=Watchman.objects.get(user_id=uid)
        all_photos=Photos.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_photos':all_photos,
                    }    
        return render(request,"myapp/view-photos.html",context)


def delete_photos(request,pk): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    pid= Photos.objects.get(id=pk)
    pid.delete() 
    return redirect("view-photos") 

def add_video(request):
    uid = User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    if request.POST:
        video_file=request.FILES['video_file']
        video_name=request.POST['video_name']
        # pic_date=request.POST['pic_date']
        vid= Video.objects.create(user_id=uid,chairman_id=cid,video_file=video_file,video_name=video_name)
        return redirect('view-video')
    else:
        context={
                    'uid':uid,
                    'cid':cid,
                }
        return render(request,"myapp/add-video.html",context)

def view_video(request):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid=Chairman.objects.get(user_id=uid)
        all_video=Video.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_video':all_video,
                    }    
        return render(request,"myapp/view-video.html",context)
    elif uid.role=="Member":
        cid=Societymember.objects.get(email=uid)
        all_video=Video.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_video':all_video,
                    }    
        return render(request,"myapp/view-video.html",context)
    elif uid.role=="watchman":
        cid=Watchman.objects.get(email=uid)
        all_video=Video.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_video':all_video,
                    }    
        return render(request,"myapp/view-video.html",context)

def delete_video(request,pk): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    pid= Video.objects.get(id=pk)
    pid.delete() 
    return redirect("view-video") 

def add_suggestion(request):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Member":
        cid= Societymember.objects.get(email=uid)
        if request.POST:
            complaints_title=request.POST['complaints_title']
            complaints_discription=request.POST['complaints_discription']
            sid= Complaints.objects.create(user_id=uid,member_id=cid,complaints_title=complaints_title,complaints_discription=complaints_discription)
            return redirect('view-suggestion')
        else:
            context={
                            'uid':uid,
                            'cid':cid,
                        }
            return render(request,"myapp/add-suggestion.html",context)
   
    
def view_suggestion(request):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid=Chairman.objects.get(user_id=uid)
        all_suggestion=Complaints.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_suggestion':all_suggestion,
                    }    
        return render(request,"myapp/view-suggestion.html",context)
    elif uid.role=="Member":
        cid = Societymember.objects.get(email=uid)
        all_suggestion = Complaints.objects.filter(user_id=uid)
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_suggestion':all_suggestion,
        }
        return render(request,"myapp/view-suggestion.html",context)



def delete_suggestion(request,sk): 
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid=Chairman.objects.get(user_id=uid)
        nid= Complaints.objects.get(id=sk)
        nid.delete() 
        return redirect("view-suggestion")
    elif uid.role=="Member":
        cid=Societymember.objects.get(email=uid)
        nid= Complaints.objects.get(id=sk)
        nid.delete() 
        return redirect("view-suggestion")
        

def add_rentsell_request(request):
    if "c_email" in request.session:
        if request.POST:
            uid = User.objects.get(email=request.session['c_email'])
            cid= Societymember.objects.get(email=uid)
            homevehicle_title=request.POST['homevehicle_title']
            homevehicle_type= request.POST['homevehicle_type']
            homevehicle_rentsell=request.POST['homevehicle_rentsell']
            homevehicle_contactno=request.POST['homevehicle_contactno']
            homevehicle_discription=request.POST['homevehicle_discription']
            homevehicle_budget=request.POST['homevehicle_budget']
            homevehicle_address_no=request.POST['homevehicle_address_no']
            homevehicle_preowned=request.POST['homevehicle_preowned']
            pic =request.FILES['pic']
            rid= Rentsell.objects.create(user_id=uid,member_id=cid,homevehicle_contactno=homevehicle_contactno,homevehicle_title=homevehicle_title,homevehicle_type=homevehicle_type,homevehicle_rentsell=homevehicle_rentsell,homevehicle_discription=homevehicle_discription,homevehicle_budget=homevehicle_budget,homevehicle_address_no=homevehicle_address_no,homevehicle_preowned=homevehicle_preowned,pic=pic)
            return redirect('view-rentsell-request')
        else:
            uid = User.objects.get(email=request.session['c_email'])
            cid = Societymember.objects.get(email=uid)
            context={
                'uid':uid,
                'cid':cid,
            }
            return render(request,"myapp/add-rentsell-request.html",context)
    else:
         return render(request,"myapp/login.html")

def view_rentsell_request(request):
    uid = User.objects.get(email=request.session['c_email'])
    cid = Societymember.objects.get(email=uid)
    all_request = Rentsell.objects.filter(user_id=uid)
    context={
                        'uid':uid,
                        'cid':cid,
                        'all_request':all_request,
        }
    return render(request,"myapp/view-rentsell-request.html",context)

def view_rentsell_all_request(request):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid = Chairman.objects.get(user_id=uid)
        all_request = Rentsell.objects.all().order_by('-created_at')[:3]
        context={
                            'uid':uid,
                            'cid':cid,
                            'all_request':all_request,
            }
        return render(request,"myapp/view-rentsell-all-request.html",context)
    elif uid.role=="Member":
        cid = Societymember.objects.get(email=uid)
        all_request = Rentsell.objects.all().order_by('-created_at')[:3]
        context={
                            'uid':uid,
                            'cid':cid,
                            'all_request':all_request,
            }
        return render(request,"myapp/view-rentsell-all-request.html",context)

def view_rentsell_request_details(request,pk):
    uid = User.objects.get(email=request.session['c_email'])
    if uid.role=="Chairman":
        cid = Chairman.objects.get(user_id=uid)
        mid= Rentsell.objects.get(id=pk)
        context={
                "uid":uid,
                "cid":cid,
                "mid":mid,
            }
        return render(request,"myapp/view-rentsell-request-details.html",context)
    elif uid.role=="Member":
        cid = Societymember.objects.get(email=uid)
        mid= Rentsell.objects.get(id=pk)
        context={
                "uid":uid,
                "cid":cid,
                "mid":mid,
            }
        return render(request,"myapp/view-rentsell-request-details.html",context)

def delete_rentsell_request(request,pk): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Societymember.objects.get(email=uid)
    nid= Rentsell.objects.get(id=pk)
    nid.delete() 
    return redirect("view-rentsell-request")


def add_maintenance(request):
    if "c_email" in request.session:
        if request.POST:
            uid = User.objects.get(email=request.session['c_email'])
            cid= Chairman.objects.get(user_id=uid)
            month=request.POST['month']
            amount= request.POST['amount']
            year= request.POST['year']
            rid= Maintenance.objects.create(user_id=uid,chairman_id=cid,year=year,month=month,amount=amount)
            return redirect('view-maintenance')
        else:
            uid = User.objects.get(email=request.session['c_email'])
            cid= Chairman.objects.get(user_id=uid)
            context={
                'uid':uid,
                'cid':cid,
            }
            return render(request,"myapp/add-maintenance.html",context)
    else:
         return render(request,"myapp/login.html")

def view_maintenance(request):
    uid = User.objects.get(email=request.session['c_email'])
   
    if uid.role=="Chairman":
        cid= Chairman.objects.get(user_id=uid)
        all_maintenance=Maintenance.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_maintenance':all_maintenance,
                    }    
        return render(request,"myapp/view-maintenance.html",context)
    if uid.role=="Member":
        cid= Societymember.objects.get(email=uid)
        all_maintenance=Maintenance.objects.all().order_by('-created_at')[:3]
        context={
                        'uid':uid,
                        'cid':cid,
                        'all_maintenance':all_maintenance,
                    }    
        return render(request,"myapp/view-maintenance.html",context)
    

def delete_maintenance(request,pk): 
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    nid= Maintenance.objects.get(id=pk)
    nid.delete() 
    return redirect("view-maintenance")

def watchman_registration(request):
    if request.POST:
        name=request.POST['name']
        contactno=request.POST['contactno']
        email=request.POST['email']
        age=request.POST['age']
        full_address=request.POST['full_address']
        uid = User.objects.create(email = email, password ="123456",role = "watchman")
        if uid.role=='watchman':
            tid= Watchman.objects.create(user_id=uid, name=name,contact_no=contactno,email=email,age=age,full_address=full_address)
            return render(request,"myapp/watchman-registration.html")
        return render(request,"myapp/watchman-registration.html")
    else:
        return render(request,"myapp/watchman-registration.html")

def watchman_approval(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid= Chairman.objects.get(user_id=uid)
    all_watchman=Watchman.objects.all()
    context={
                        'uid':uid,
                        'cid':cid,
                        'all_watchman':all_watchman,
                    } 
    return render(request,"myapp/watchman-approval.html",context)

   