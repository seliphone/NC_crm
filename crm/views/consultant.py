from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib import auth
from django.views import View
from PIL import Image,ImageDraw,ImageFont
import random
from io import BytesIO
from crm.forms import RegForm
# djsflkjsghfhfhh

# 验证码
def random_color():                                # 定义一个生成随机颜色代码的函数
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)
def v_code(request):                               # 专门返回验证码图片的视图函数
    # 创建一个随机颜色的图片对象
    img_obj = Image.new('RGB',(250,35),random_color())
    # 在该图片对象上生成一个画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载一个字体对象
    font_obj = ImageFont.truetype('static/font/kumo.ttf',28)
    temp = []
    for i in range(5):
        l = chr(random.randint(97,122))             #小写字母
        b = chr(random.randint(65,90))              #大写字母
        n = str(random.randint(0,9))                #数字
        # 从上面三个随机选一个
        t = random.choice([l,b,n])
        temp.append(t)
        # 将选中过的那个字符写到图片上
        draw_obj.text((i * 40 + 35,0),t,fill=random_color(),font=font_obj)
    # 将生成的验证码保存
    request.session['v_code'] = ''.join(temp).upper()
    # 直接在内存中保存图片替代io操作
    f1 = BytesIO()
    img_obj.save(f1,format="PNG")
    img_data = f1.getvalue()
    return HttpResponse(img_data ,content_type='image/png')
# 登录
def login(request):
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        v_code = request.POST.get('v_code','').upper()
        if v_code == request.session.get('v_code'):
            obj = auth.authenticate(request ,username=username ,password=password)
            if obj:

                return redirect(reverse('my_customer'))
            err_msg = '用户名或密码错误'
        else:
            err_msg = '验证码错误'


    return render(request ,'login.html',{'err_msg':err_msg})
# 注册
def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # 创建新用户
            obj = form_obj.save()
            obj.set_password(obj.password)
            obj.save()
            return redirect('/login/')
    return render(request ,'reg.html',{'form_obj':form_obj})

class CustomerList(View):
    def get(self,request):
        return render(request,'crm/consultant/customer_list.html')
