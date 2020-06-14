from django.shortcuts import render
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import customer_voice_model,user_meta,qa_model,catalog_model
import os

from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
import json



#line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)

json_list={
  "destination": "xxxxxxxxxx",
  "events": [
    {
      "replyToken": "8cf9239d56244f4197887e939187e19e",
      "type": "follow",
      "mode": "active",
      "timestamp": 1462629479859,
      "source": {
        "type": "user",
        "userId": "U4af4980629..."
      }
    }
  ]
}

#line_user_id = events[0]['source']['userId']
#if events[0]['type'] == 'message':
#    text = request_json['events'][0]['message']['text']
#    line_bot_api.push_message(line_user_id, TextSendMessage(text='Hello World!'))

@csrf_exempt
def callback_view(request):
    YOUR_CHANNEL_ACCESS_TOKEN ='52+twonMXh6ueH20i0f0J0mIYNom107nAwJnXiZyB4DwwSvN/NwKN6JiEn+kECPjHZHZeZqyFmLNwwb4GbjoIs10FaT0PXQnWvU6ic35ua33q1F984zYr+hy8imDUy67Gjjk58+YEmbNz7wqEI5uywdB04t89/1O/w1cDnyilFU='
    YOUR_CHANNEL_SECRET='72b96cff52e8346263319984f3955e2c'
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
    parser = WebhookParser(YOUR_CHANNEL_SECRET)
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    try:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=str(event.source.userId))
                        )
                    except LineBotApiError as e:
                        print(e.status_code)
                        print(e.error.message)
                        print(e.error.details)


                try:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=str(event.type))
                    )
                except :
                    pass

            if event.type =="follow":
                try:
                    line_bot_api.reply_message(
                        event.replyToken,
                        TextSendMessage(text=str(events))
                    )
                except LineBotApiError as e:
                    print(e.status_code)
                    print(e.error.message)
                    print(e.error.details)



        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def callback(request):

    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        line_user_id = events[0]['source']['userId']

        # 友達追加時
        if events[0]['type'] == 'follow':
            profile = line_bot_api.get_profile(line_user_id)
            line_bot_api.push_message(line_user_id, TextSendMessage(text='Hello World!'))

        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            pass

        # メッセージ受信時
        elif events[0]['type'] == 'message':
            text = request_json['events'][0]['message']['text']
            line_bot_api.push_message('U3ef4b863f370e1971bbc243ddc9d861c', TextSendMessage(text='Hello World!'))

    return HttpResponse("ok")


# Create your views here.
def login_view(request):
    return redirect('regi')

def logout_view(request):
    logout(request)
    return redirect(to='index')

def index_view(request):
    YOUR_CHANNEL_ACCESS_TOKEN ='52+twonMXh6ueH20i0f0J0mIYNom107nAwJnXiZyB4DwwSvN/NwKN6JiEn+kECPjHZHZeZqyFmLNwwb4GbjoIs10FaT0PXQnWvU6ic35ua33q1F984zYr+hy8imDUy67Gjjk58+YEmbNz7wqEI5uywdB04t89/1O/w1cDnyilFU='
    YOUR_CHANNEL_SECRET='72b96cff52e8346263319984f3955e2c'
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
    a='U3ef4b863f370e1971bbc243ddc9d861c'
    line_bot_api.push_message(request.user.uid, TextSendMessage(text='Hello World!'))
    cv=customer_voice_model.objects.all()
    params={
        'ccc':cv,
    }
    return render(request,'tosou/index.html',params)


def check_view(request):
    if request.method == 'POST':
        params={
            'rate_true':False,
            'sai':'',
            'riritu':'',
            'kikan':'',
            'hoho':'',
            'new_rate':'',
            'now_tuki':'',
            'now_nen':'',
            'now_total':'',
            'after_tuki':'',
            'after_nen':'',
            'after_total':'',
            'tuki_sa':'',
            'nen_sa':'',
            'total_sa':'',
        }
        try:
            gaku=request.POST['gaku']
        except:
            gaku='no'
        try:
            nen=request.POST['nen']
        except:
            nen='no'
        try:
            risi=request.POST['risi']
        except:
            risi='no'
        if gaku=='on' and nen=='on' and risi == 'on':
            return render(request,'tosou/nai.html',params)
        elif gaku == 'on' and nen == 'on':
            return render(request,'tosou/nai.html',params)
        elif gaku == 'on' and risi == 'on':
            return render(request,'tosou/nai.html',params)
        elif nen == 'on' and risi == 'on':
            return render(request,'tosou/nai.html',params)
        else:
            return redirect('present')

def easy_view(request):
    if request.method == 'POST':
        zangaku=int(request.POST['sai'])
        rate=float(request.POST['riritu'])*0.01/12
        kaisu=int(request.POST['kikan'])*12
        rate1=1+rate
        kaisu1=kaisu-1
        hoho=int(request.POST['hensai'])
        params={
            'sai':int(request.POST['sai']),
            'riritu':float(request.POST['riritu']),
            'kikan':int(request.POST['kikan']),
            'hoho':int(request.POST['hensai']),
            'new_rate':float(request.POST['new_rate']),
            'rate_true':True,
            'now_tuki':'',
            'now_nen':'',
            'now_total':'',
            'after_tuki':'',
            'after_nen':'',
            'after_total':'',
            'tuki_sa':'',
            'nen_sa':'',
            'total_sa':'',
        }
        ####################now#########################
        if hoho == 1:
            #元利均等返済の毎月返済額
            tuki=zangaku*rate/(1-rate1**(-kaisu))
            now_tuki=round(tuki)
            #元利均等返済における支払利息の合計金額 ＝ 借入金額 ×（返済回数 × 利率 ÷（1 －（1 ＋ 利率）＾（－返済回数））－ 1）
            now_nen=now_tuki*12
            now_total=zangaku*(kaisu*rate/(1-(1+rate)**(-kaisu))-1)
            params['now_tuki']="{:,d}".format(now_tuki)
            params['now_nen']="{:,d}".format(now_nen)
            params['now_total']="{:,d}".format(round(now_total))

        else:
            #元金均等返済の毎月返済額
            l_list=[]
            for x in range(1,kaisu):
                a=zangaku/kaisu
                tutu=zangaku/kaisu*(1+kaisu-x+1)*rate
                atu=a+tutu
                atu=round(atu)
                l_list.append(atu)
            now_tuki=l_list[0]
            now_nen=0
            for n in range(0,11):
                now_nen += int(l_list[n])
            #元金均等返済における支払利息の合計金額 ＝ 借入金額 × 利率 ×（返済回数 ＋ 1）÷ 2
            now_total=zangaku*rate*(kaisu+1)/2
            params['now_tuki']="{:,d}".format(now_tuki)
            params['now_nen']="{:,d}".format(now_nen)
            params['now_total']="{:,d}".format(round(now_total))
        ####################after#########################
        new_rate=float(request.POST['new_rate'])*0.01/12
        rate1=1+new_rate
        if hoho == 1:
            #元利均等返済の毎月返済額
            after_tuki=zangaku*new_rate/(1-rate1**(-kaisu))
            after_tuki=round(after_tuki)
            #元利均等返済における支払利息の合計金額 ＝ 借入金額 ×（返済回数 × 利率 ÷（1 －（1 ＋ 利率）＾（－返済回数））－ 1）
            after_nen=after_tuki*12
            after_total=zangaku*(kaisu*new_rate/(1-(1+new_rate)**(-kaisu))-1)
            params['after_tuki']="{:,d}".format(after_tuki)
            params['after_nen']="{:,d}".format(after_nen)
            params['after_total']="{:,d}".format(round(after_total))

        else:
            #元金均等返済の毎月返済額
            after_list=[]
            for x in range(1,kaisu):
                a=zangaku/kaisu
                tutu=zangaku/kaisu*(1+kaisu-x+1)*new_rate
                atu=a+tutu
                atu=round(atu)
                after_list.append(atu)
            after_tuki=after_list[0]
            after_nen=0
            for n in range(0,11):
                after_nen += int(after_list[n])
            #元金均等返済における支払利息の合計金額 ＝ 借入金額 × 利率 ×（返済回数 ＋ 1）÷ 2
            after_total=zangaku*new_rate*(kaisu+1)/2
            params['after_tuki']="{:,d}".format(after_tuki)
            params['after_nen']="{:,d}".format(after_nen)
            params['after_total']="{:,d}".format(round(after_total))
        ##################################################
        tuki_sa=after_tuki-now_tuki
        nen_sa=after_nen-now_nen
        total_sa=after_total-now_total
        params['tuki_sa']="{:,d}".format(abs(tuki_sa))
        params['nen_sa']="{:,d}".format(abs(nen_sa))
        params['total_sa']="{:,d}".format(abs(round(total_sa)))

        return render(request,'tosou/nai.html',params)

def a_easy_view(request):
    if request.method == 'POST':
        zangaku=int(request.POST['sai'])
        rate=float(request.POST['riritu'])*0.01/12
        kaisu=int(request.POST['kikan'])*12
        rate1=1+rate
        kaisu1=kaisu-1
        hoho=int(request.POST['hensai'])
        params={
            'sai':int(request.POST['sai']),
            'riritu':float(request.POST['riritu']),
            'kikan':int(request.POST['kikan']),
            'hoho':int(request.POST['hensai']),
            'new_rate':float(request.POST['new_rate']),
            'rate_true':True,
            'now_tuki':'',
            'now_nen':'',
            'now_total':'',
            'after_tuki':'',
            'after_nen':'',
            'after_total':'',
            'tuki_sa':'',
            'nen_sa':'',
            'total_sa':'',
        }
        ####################now#########################
        if hoho == 1:
            #元利均等返済の毎月返済額
            tuki=zangaku*rate/(1-rate1**(-kaisu))
            now_tuki=round(tuki)
            #元利均等返済における支払利息の合計金額 ＝ 借入金額 ×（返済回数 × 利率 ÷（1 －（1 ＋ 利率）＾（－返済回数））－ 1）
            now_nen=now_tuki*12
            now_total=zangaku*(kaisu*rate/(1-(1+rate)**(-kaisu))-1)
            params['now_tuki']="{:,d}".format(now_tuki)
            params['now_nen']="{:,d}".format(now_nen)
            params['now_total']="{:,d}".format(round(now_total))

        else:
            #元金均等返済の毎月返済額
            l_list=[]
            for x in range(1,kaisu):
                a=zangaku/kaisu
                tutu=zangaku/kaisu*(1+kaisu-x+1)*rate
                atu=a+tutu
                atu=round(atu)
                l_list.append(atu)
            now_tuki=l_list[0]
            now_nen=0
            for n in range(0,11):
                now_nen += int(l_list[n])
            #元金均等返済における支払利息の合計金額 ＝ 借入金額 × 利率 ×（返済回数 ＋ 1）÷ 2
            now_total=zangaku*rate*(kaisu+1)/2
            params['now_tuki']="{:,d}".format(now_tuki)
            params['now_nen']="{:,d}".format(now_nen)
            params['now_total']="{:,d}".format(round(now_total))
        ####################after#########################
        new_rate=float(request.POST['new_rate'])*0.01/12
        rate1=1+new_rate
        if hoho == 1:
            #元利均等返済の毎月返済額
            after_tuki=zangaku*new_rate/(1-rate1**(-kaisu))
            after_tuki=round(after_tuki)
            #元利均等返済における支払利息の合計金額 ＝ 借入金額 ×（返済回数 × 利率 ÷（1 －（1 ＋ 利率）＾（－返済回数））－ 1）
            after_nen=after_tuki*12
            after_total=zangaku*(kaisu*new_rate/(1-(1+new_rate)**(-kaisu))-1)
            params['after_tuki']="{:,d}".format(after_tuki)
            params['after_nen']="{:,d}".format(after_nen)
            params['after_total']="{:,d}".format(round(after_total))

        else:
            #元金均等返済の毎月返済額
            after_list=[]
            for x in range(1,kaisu):
                a=zangaku/kaisu
                tutu=zangaku/kaisu*(1+kaisu-x+1)*new_rate
                atu=a+tutu
                atu=round(atu)
                after_list.append(atu)
            after_tuki=after_list[0]
            after_nen=0
            for n in range(0,11):
                after_nen += int(after_list[n])
            #元金均等返済における支払利息の合計金額 ＝ 借入金額 × 利率 ×（返済回数 ＋ 1）÷ 2
            after_total=zangaku*new_rate*(kaisu+1)/2
            params['after_tuki']="{:,d}".format(after_tuki)
            params['after_nen']="{:,d}".format(after_nen)
            params['after_total']="{:,d}".format(round(after_total))
        ##################################################
        tuki_sa=after_tuki-now_tuki
        nen_sa=after_nen-now_nen
        total_sa=after_total-now_total
        params['tuki_sa']="{:,d}".format(abs(tuki_sa))
        params['nen_sa']="{:,d}".format(abs(nen_sa))
        params['total_sa']="{:,d}".format(abs(round(total_sa)))

        return render(request,'tosou/account.html',params)

def consul_form_view(request):
    return render(request,'tosou/consul.html')

def email_view(request):
    if request.method=='POST':
        afi=request.POST['afi']
        check=request.POST['check']
        hurigana=request.POST['hurigana']
        name=request.POST['name']
        old=request.POST['old']
        yubin=request.POST['yubin']
        stay=request.POST['stay']
        email=request.POST['email']
        tel=request.POST['tel']
        one_day=request.POST['one_day']
        one=request.POST['one']
        if one == '1':
            one='9:00-12:00'
        elif one =='2':
            one='12:00-15:00'
        elif one == '3':
            one='15:00-18:00'
        else:
            one='18:00-20:00'
        two_day=request.POST['two_day']
        two=request.POST['two']
        if two == '1':
            two='9:00-12:00'
        elif two =='2':
            two='12:00-15:00'
        elif two == '3':
            two='15:00-18:00'
        else:
            two='18:00-20:00'
        kinri=request.POST['kinri']
        if kinri=='1':
            k_more='1.5%以上'
        elif kinri== '2':
            k_more='1.5%未満'
        elif kinri == '3' :
            k=request.POST['k_more']
            k_more=str(k)+'%'
        zansai=request.POST['zansai']
        if zansai =='1':
            s_more='1000万円以上'
        elif zansai=='2':
            s_more='1000万円未満'
        elif zansai == '3':
            s=request.POST['s_more']
            s_more=str(s)+'万円'
        zannen=request.POST['zannen']
        if zannen =='1':
            n_more='10年以上'
        elif zannen=='2':
            n_more='10年未満'
        elif zannen =='3':
            n=request.POST['n_more']
            n_more=str(n)+'年'
        nensyu=request.POST['nensyu']
        if nensyu == '1':
            nensyu='400万円以上'
        else:
            nensyu='400万円未満'

        email_msg=hurigana+'\n'+name+'\n'+str(old)+'歳\n'+str(yubin)+'\n'+stay+'\n電話番号'+tel+'\n'+'メールアドレス'+email+'\n'+'第一希望:'+str(one_day)+'\n'+one+'\n第二希望:'+str(two_day)+'\n'+two+'\n'+'現行金利'+k_more+'\n残債額'+s_more+'\n残年数'+n_more+'\n年収'+nensyu

        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(os.environ['mymail'], os.environ['mymailpass'])
        msg = MIMEText(email_msg)

        msg['Subject'] = 'subject'
        msg['From'] = os.environ['mymail']
        msg['To'] = 'keito3261998@gmail.com'
        msg['Date'] = formatdate()
        smtpobj.sendmail(os.environ['mymail'], 'keito3261998@gmail.com', msg.as_string())
        smtpobj.close()


        return redirect('complete')
    return redirect('easy')

def complete_view(request):
    return render(request,'tosou/account.html')

def good_view(request):
    return render(request,'tosou/account.html')

def present_view(request):
    return render(request,'tosou/gai.html')

def mitumori_view(request):
    return render(request,'tosou/mitumori.html')

def e_s_view(request):
    return render(request,'tosou/nai.html')

def page_view(request):
    return render(request,'tosou/page.html')

def renovation_view(request):
    return render(request,'tosou/renovation.html')

def line_view(request):
    return render(request,'tosou/ful_contact.html')

def qa_view(request):
    qa_list=qa_model.objects.all()
    params={
        'aaa':qa_list,
    }
    return render(request,'tosou/qa.html',params)

def catalog_view(request):
    catalog=catalog_model.objects.all()
    params={
        'ccc':catalog,
    }
    return render(request,'tosou/catalog.html',params)


def m_form_view(request):
    if request.method=='POST':
        hurigana=request.POST['hurigana']
        name=request.POST['name']
        yubin=request.POST['yubin']
        stay=request.POST['stay']
        email=request.POST['email']
        tel=request.POST['tel']
        question_area=request.POST['question_area']
        one_day=request.POST['one_day']
        one=request.POST['one']
        if one == '1':
            one='9:00-12:00'
        elif one =='2':
            one='12:00-15:00'
        elif one == '3':
            one='15:00-18:00'
        else:
            one='18:00-20:00'
        two_day=request.POST['two_day']
        two=request.POST['two']
        if two == '1':
            two='9:00-12:00'
        elif two =='2':
            two='12:00-15:00'
        elif two == '3':
            two='15:00-18:00'
        else:
            two='18:00-20:00'

        email_msg=hurigana+'\n'+name+'\n'+yubin+'\n'+stay+'\n'+email+'\n'+tel+'\n'+one_day+one+'\n'+two_day+two+'\n'+'\n'+question_area

        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(os.environ['mymail'], os.environ['mymailpass'])
        msg = MIMEText(email_msg)

        msg['Subject'] = 'subject'
        msg['From'] = 'sss.tl.ges.sss@gmail.com'
        msg['To'] = 'keito3261998@gmail.com'
        msg['Date'] = formatdate()
        smtpobj.sendmail(os.environ['mymail'], 'keito3261998@gmail.com', msg.as_string())
        smtpobj.close()

        return redirect('good')
    return redirect('index')

def regi_view(request):
    return render(request,'tosou/regi.html')

@login_required
def account_view(request):
    user=request.user
    params={
        'afi_code':'',
        'line_regi':'',
    }
    try:
        meta=user_meta.objects.get(user=user)
    except:
        params['line_regi']=False
    else:
        params['line_regi']=True
        params['afi_code']=meta.afi_code
    return render(request,'tosou/account.html',params)
