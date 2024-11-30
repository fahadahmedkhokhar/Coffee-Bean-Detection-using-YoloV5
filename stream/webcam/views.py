from django.shortcuts import render,redirect,get_object_or_404
from django.http import StreamingHttpResponse
import yolov5,torch
from utils.general import (check_img_size, non_max_suppression,
                                  check_imshow, xyxy2xywh, increment_path)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
import cv2
from django.contrib.auth import authenticate, login
import pathlib
from webcam.forms import AddAccountForm
from webcam.models import Account
from PIL import Image as im
# Create your views here.


def dashboard(request):
    return render(request, 'Dashboard.html')

def livestream(request):
    return render(request, 'live_stream.html')

def contact(request):
    return render(request, 'Contact.html')

def about(request):
    return render(request, 'About.html')

def employee_main(request):
    return render(request, 'EmployeeMain.html')

def add_employee(request):
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        print(form.errors)
        if form.is_valid():
            Account.objects.create(
                uname=form.cleaned_data['uname'],
                name=form.cleaned_data['name'],
                psw=form.cleaned_data['psw'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
            )
            print(form.cleaned_data['email'])
            return redirect('main/admin_main')  # Redirect to a success page
    else:
        form = AddAccountForm()
        print(form.errors)
    # return render(request, 'your_template.html', {'form': form})
    return render(request, 'AddAccount.html')

def delete_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    account.delete()
    return redirect('main/admin_main')
def update_employee(request, account_id):
    account = Account.objects.get(id=account_id)
    form = AddAccountForm(request.POST, instance = account)
    if form.is_valid():
        form.save()
        return redirect("main/admin_main")
    return render(request, 'UpdateAccount.html', {'account': account})

def index(request):
    return render(request,'Homepage.html')
def admin_main(request):
    accounts = Account.objects.all()
    return render(request, 'ManageAccount.html', {'accounts': accounts})

def admin_all(request):
    return render(request, 'AdminMain.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        if username == 'admin' and password == 'admin':
            return redirect('main/admin_all')
        else:
            try:
                account = Account.objects.get(uname=username)
                if username == account.uname and password == account.psw:
                    return redirect('main/employee')
            except Account.DoesNotExist:
                pass  # Username not found
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to the main dashboard or another page after successful login
            return redirect('main/employee')  # Replace 'main_dashboard' with your main dashboard URL name
        else:
            # Return an 'invalid login' error message.
            return render(request, 'Login.html', {'error_message': 'Invalid username or password'})
    else:
        # If the request method is not POST, render the login form.
        return render(request, 'Login.html')



temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

print(torch.cuda.is_available())
#load model
model = yolov5.load("best_1.pt")
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
device = select_device('') # 0 for gpu, '' for cpu
# initialize deepsort
cfg = get_config()
cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
# cfg.merge_from_file("stream/trained_model/Bunnah-13/data.yaml")
deepsort = DeepSort('osnet_x0_25',
                    device,
                    max_dist=cfg.DEEPSORT.MAX_DIST,
                    max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    )
# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names

def stream():
    cap = cv2.VideoCapture(0)
    model.conf = 0.2
    model.iou = 0.4
    model.classes = [0,1,2,3,4,5]
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break

        results = model(frame, augment=True)
        # proccess
        annotator = Annotator(frame, line_width=2, pil=not ascii) 
        det = results.pred[0]
        if det is not None and len(det):   
            xywhs = xyxy2xywh(det[:, 0:4])
            confs = det[:, 4]
            clss = det[:, 5]
            outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss.cpu(), frame)
            if len(outputs) > 0:
                for j, (output, conf) in enumerate(zip(outputs, confs)):

                    bboxes = output[0:4]
                    id = output[4]
                    cls = output[5]

                    c = int(cls)  # integer class
                    label = f'{id} {names[c]} {conf:.2f}'
                    annotator.box_label(bboxes, label, color=colors(c, True))

        else:
            deepsort.increment_ages()

        im0 = annotator.result()    
        image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')    