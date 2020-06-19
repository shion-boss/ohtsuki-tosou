from django.shortcuts import render
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import customer_voice_model,user_meta,qa_model,catalog_model,message_table_model,message_user_model,account_meta,code_model,c_v_model
import datetime
import random
import os
from allauth.socialaccount.models import SocialAccount
from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
import json
import requests

line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)
parser = WebhookParser(settings.YOUR_CHANNEL_SECRET)


#line_user_id = events[0]['source']['userId']
#if events[0]['type'] == 'message':
#    text = request_json['events'][0]['message']['text']
#    line_bot_api.push_message(line_user_id, TextSendMessage(text='Hello World!'))


@csrf_exempt
def callback_view(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        line_user_id = events[0]['source']['userId']

        # チャネル設定のWeb hook接続確認時にはここ。このIDで見に来る。
        if line_user_id == 'Udeadbeefdeadbeefdeadbeefdeadbeef':
            pass

        elif events[0]['type'] == 'message':
            text=event[0]['message']['text']
            headers = {
                'Authorization': 'Bearer '+settings.YOUR_CHANNEL_ACCESS_TOKEN,
            }
            request_url='https://api.line.me/v2/bot/profile/'+str(line_user_id)
            r = requests.get(request_url, headers=headers)
            data = json.loads(r.text)
            name=data["displayName"]
            message=name+'様から公式アカウントへお問い合わせがありました。\n'+'【お問い合わせ内容】\n'+text
            line_bot_api.push_message("Uff0e2cefe508240835a59e0f069e0922", TextSendMessage(text=message))
            line_bot_api.push_message("U0b64c93b9b15663616d71a057cd41b38", TextSendMessage(text=message))
            line_bot_api.push_message("U8d5974a689241759e8e95f05f161e9bb", TextSendMessage(text=message))
            line_bot_api.push_message("U3ef4b863f370e1971bbc243ddc9d861c", TextSendMessage(text=message))
            table=message_table_model.objects.get(title=line_user_id)
            meta=user_meta.objects.get(uid=line_user_id)
            u_text=message_user_model(title=table,uid=line_user_id,message=text)
            u_text.save()


        # 友達追加時・ブロック解除時
        elif events[0]['type'] == 'follow':
            try:
                message_table_model.objects.get(title=line_user_id)
            except:
                message_table_model(title=line_user_id).save()
            if SocialAccount.objects.filter(uid=line_user_id).exists():
                account=SocialAccount.objects.get(uid=line_user_id)
                try:
                    user_meta.objects.get(uid=line_user_id)
                except:
                    #サイトからのユーザー登録
                    headers = {
                        'Authorization': 'Bearer '+settings.YOUR_CHANNEL_ACCESS_TOKEN,
                    }
                    request_url='https://api.line.me/v2/bot/profile/'+str(line_user_id)
                    r = requests.get(request_url, headers=headers)
                    data = json.loads(r.text)
                    name=data["displayName"]
                    top=data['pictureUrl']
                    code=code_model.objects.get(option=0)
                    afi_code='{:0=6}'.format(int(code.num))
                    code.num+=1
                    code.save()
                    meta=user_meta(username=str(name),top=str(top),afi_code=str(afi_code),uid=str(line_user_id))
                    meta.save()
                else:
                    #ブロック解除のユーザー
                    meta=user_meta.objects.get(uid=str(line_user_id))
                    afi_code=meta.afi_code
            else:
                #lineを直接追加したユーザー
                headers = {
                    'Authorization': 'Bearer '+settings.YOUR_CHANNEL_ACCESS_TOKEN,
                }
                request_url='https://api.line.me/v2/bot/profile/'+str(line_user_id)
                r = requests.get(request_url, headers=headers)
                data = json.loads(r.text)
                name=data["displayName"]
                top=data['pictureUrl']
                code=code_model.objects.get(option=0)
                afi_code='{:0=6}'.format(int(code.num))
                code.num+=1
                code.save()
                meta=user_meta(username=str(name),top=str(top),afi_code=str(afi_code),uid=str(line_user_id))
                meta.save()

            headers = {
                'Authorization': 'Bearer '+settings.YOUR_CHANNEL_ACCESS_TOKEN,
            }
            request_url='https://api.line.me/v2/bot/profile/'+str(line_user_id)
            r = requests.get(request_url, headers=headers)
            data = json.loads(r.text)
            name=data["displayName"]
            top=data['pictureUrl']
            welcome='大槻塗装公式LINEをご登録いただきありがとうございます。\n\n現金負担0円塗装をより多くの方々にお届けするために、\nお仕事をご紹介してくださった方、お仕事を依頼してくださった方へ、感謝の気持ちを込めて、紹介特典としてプレゼント企画を始めました。\n'+str(name)+'様限定の紹介コードは「'+str(afi_code)+'」です。\n紹介特典のカタログや現金負担0円塗装の詳細は、下記URLにてご覧ください。\n'+'https://www.ohtsuki-tosou.com'
            #message to user
            line_bot_api.push_message(str(line_user_id), TextSendMessage(text=welcome))

            #message to staff
            message=str(name)+'さんが新規LINE登録しました！！！！'
            line_bot_api.push_message("Uff0e2cefe508240835a59e0f069e0922", TextSendMessage(text=message))
            line_bot_api.push_message("U0b64c93b9b15663616d71a057cd41b38", TextSendMessage(text=message))
            line_bot_api.push_message("U8d5974a689241759e8e95f05f161e9bb", TextSendMessage(text=message))
            line_bot_api.push_message("U3ef4b863f370e1971bbc243ddc9d861c", TextSendMessage(text=message))

        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            #message to staff
            line_bot_api.push_message("Uff0e2cefe508240835a59e0f069e0922", TextSendMessage(text='ブロックされました。'))


    return HttpResponse()


# Create your views here.
def login_view(request):
    return redirect('regi')

def logout_view(request):
    logout(request)
    return redirect(to='index')

def tirasi_index_view(request):
    cv=c_v_model.objects.all()
    params={
        'ccc':cv,
        "afi_code":'000000',
    }
    if settings.DEBUG==False:
        if request.user.is_authenticated:
            try:
                social_account=SocialAccount.objects.get(user=request.user)
            except:
                pass
            else:
                try:
                    meta=user_meta.objects.get(uid=social_account.uid)
                except:
                    params['afi_code']='000000'
                else:
                    params['afi_code']=meta.afi_code
    return render(request,'tosou/index.html',params)

def web_index_view(request):
    cv=c_v_model.objects.all()
    params={
        'ccc':cv,
        "afi_code":'000000',
    }
    if settings.DEBUG==False:
        if request.user.is_authenticated:
            try:
                social_account=SocialAccount.objects.get(user=request.user)
            except:
                pass
            else:
                try:
                    meta=user_meta.objects.get(uid=social_account.uid)
                except:
                    params['afi_code']='000000'
                else:
                    params['afi_code']=meta.afi_code
    return render(request,'tosou/index.html',params)

def index_view(request):
    cv=c_v_model.objects.all()
    params={
        'ccc':cv,
        "afi_code":'000000',
    }
    if settings.DEBUG==False:
        if request.user.is_authenticated:
            try:
                social_account=SocialAccount.objects.get(user=request.user)
            except:
                pass
            else:
                try:
                    meta=user_meta.objects.get(uid=social_account.uid)
                except:
                    params['afi_code']='000000'
                else:
                    params['afi_code']=meta.afi_code
    return render(request,'tosou/index.html',params)


def voice_form_view(request):
    if request.method=='POST':
        if settings.DEBUG==False:
            if request.user.is_authenticated:
                try:
                    social_account=SocialAccount.objects.get(user=request.user)
                except:
                    pass
                else:
                    uid=social_account.uid
                    try:
                        not_pic=request.POST['not_pic']
                    except:
                        not_pic='not_on'
                    voice=request.POST['voice']
                    headers = {
                        'Authorization': 'Bearer '+settings.YOUR_CHANNEL_ACCESS_TOKEN,
                    }
                    request_url='https://api.line.me/v2/bot/profile/'+str(uid)
                    r = requests.get(request_url, headers=headers)
                    data = json.loads(r.text)
                    top=data['pictureUrl']
                    if not_pic =='on':
                        pic_list=[
                        'https://res.cloudinary.com/hlbrfvwak/image/upload/v1592458130/account-blue_xuo3jn.png',
                        'https://res.cloudinary.com/hlbrfvwak/image/upload/v1592458134/account-green_sqqiu2.png',
                        'https://res.cloudinary.com/hlbrfvwak/image/upload/v1592458151/account-orange_vkeuqy.png',
                        'https://res.cloudinary.com/hlbrfvwak/image/upload/v1592458157/account-pink_k3iuul.png',
                        'https://res.cloudinary.com/hlbrfvwak/image/upload/v1592458162/account-yellow_jgvcvi.png',
                        'https://res.cloudinary.com/hlbrfvwak/image/upload/v1592166538/gpm3ei8ydcd11j6u4x8z.png'
                        ]
                        top=random.choise(pic_list)
                        cv=c_v_model(pic=top,voice=voice)
                    else:
                        cv=c_v_model(pic=top,voice=voice)
                    cv.save()

    return redirect('index')

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
            'afi_code':'',
        }
        try:
            social_account=SocialAccount.objects.get(user=request.user)
            meta=user_meta.objects.get(uid=social_account.uid)
        except:
            params['afi_code']='000000'
        else:
            params['afi_code']=meta.afi_code
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
        if request.POST['sai']=='':
            zangaku=int(request.POST['n_sai'])
        else:
            zangaku=int(request.POST['sai'])
        rate=float(request.POST['riritu'])*0.01/12
        kaisu=int(request.POST['kikan'])*12
        rate1=1+rate
        kaisu1=kaisu-1
        hoho=int(request.POST['hensai'])
        params={
            'sai':int(zangaku),
            'n_sai':int(zangaku),
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
            'afi_code':'',
        }
        try:
            social_account=SocialAccount.objects.get(user=request.user)
            meta=user_meta.objects.get(uid=social_account.uid)
        except:
            params['afi_code']='000000'
        else:
            params['afi_code']=meta.afi_code
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
        try:
            zangaku=int(request.POST['sai'])
        except:
            pass
        try:
            zangaku=int(request.POST['n_sai'])
        except:
            pass
        rate=float(request.POST['riritu'])*0.01/12
        kaisu=int(request.POST['kikan'])*12
        rate1=1+rate
        kaisu1=kaisu-1
        hoho=int(request.POST['hensai'])
        params={
            'sai':int(zangaku),
            'n_sai':int(zangaku),
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
            'afi_code':'',
        }
        try:
            social_account=SocialAccount.objects.get(user=request.user)
            meta=user_meta.objects.get(uid=social_account.uid)
        except:
            params['afi_code']='000000'
        else:
            params['afi_code']=meta.afi_code
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
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/consul.html',params)

#無料相談
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
        o_d = datetime.datetime.strptime(one_day, '%Y-%m-%d')
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
        t_d = datetime.datetime.strptime(two_day, '%Y-%m-%d')
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

        #to customer
        email_msg=(
            "お問い合わせの送信が完了しました。\n"
            "担当の者からの連絡をお待ちください。\n"
            "=============================\n"
            "▽お問い合わせ内容\n"
            "=============================\n"
            "\n【おなまえ】\n"
            +str(hurigana)+
            "\n【お名前】\n"
            +str(name)+
            "\n【ご年齢】\n"
            +str(old)+'歳'
            "\n【郵便番号】\n"
            +str(yubin)+
            "\n【ご住所】\n"
            +str(stay)+
            "\n【メールアドレス】\n"
            +str(email)+
            "\n【お電話番号】\n"
            +str(tel)+
            "\n【連絡希望日時】\n"
            "<第一希望>\n"
            +str(o_d.year)+'年'+str(o_d.month)+'月'+str(o_d.day)+'日'+str(one)+
            "\n<第二希望>\n"
            +str(t_d.year)+'年'+str(t_d.month)+'月'+str(t_d.day)+'日'+str(two)+
            "\n【現行金利】\n"
            +str(k_more)+
            "\n【残債額】\n"
            +str(s_more)+
            "\n【残年数】\n"
            +str(n_more)+
            "\n【年収】\n"
            +str(nensyu)+
            "\n【紹介コード】\n"
            +str(afi)+
            "\n"
            "\n===========================\n"
            "このメールはお客様が大槻塗装工業のホームページから"
            "送信したものを自動でお送りしています。\n"
            "希望の連絡日時に沿えなかった際は、"
            "メールにて再度連絡希望日時をご確認させていただくことをご了承ください。\n"
            "=============================\n"
            "有限会社大槻塗装工業\n"
            "〒238-0032 神奈川県横須賀市平作2-20-2\n"
            "Tel 090-2564-5015\n"
            "email info@ohtsuki-tosou.ne.jp\n"
            "HP  https://www.ohtsuki-tosou.co.jp/\n"
            "LP https://www.ohtsuki-tosou.com/\n"
            "=============================\n"
        )

        #to customer
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(settings.MYMAIL, settings.MYMAILPASS)
        msg = MIMEText(email_msg)

        msg['Subject'] = '無料相談のお問い合わせ'
        msg['From'] = settings.MYMAIL
        msg['To'] = email
        msg['Date'] = formatdate()
        smtpobj.sendmail(settings.MYMAIL, email, msg.as_string())
        smtpobj.close()


        email_msg=("スマートリノベーション様\n"
            "加盟店の有限会社大槻塗装工業です。\n"
            "お世話になっております。\n"
            "お客様より無料相談のお問い合わせがありました。\n"
            "=============================\n"
            "▽お問い合わせ内容\n"
            "=============================\n"
            "\n【おなまえ】\n"
            +str(hurigana)+
            "\n【お名前】\n"
            +str(name)+
            "\n【ご年齢】\n"
            +str(old)+'歳'
            "\n【郵便番号】\n"
            +str(yubin)+
            "\n【ご住所】\n"
            +str(stay)+
            "\n【メールアドレス】\n"
            +str(email)+
            "\n【お電話番号】\n"
            +str(tel)+
            "\n【連絡希望日時】\n"
            "<第一希望>\n"
            +str(o_d.year)+'年'+str(o_d.month)+'月'+str(o_d.day)+'日'+str(one)+
            "\n<第二希望>\n"
            +str(t_d.year)+'年'+str(t_d.month)+'月'+str(t_d.day)+'日'+str(two)+
            "\n【現行金利】\n"
            +str(k_more)+
            "\n【残債額】\n"
            +str(s_more)+
            "\n【残年数】\n"
            +str(n_more)+
            "\n【年収】\n"
            +str(nensyu)+
            "\n"
            "=============================\n"
            "このメールはお客様が大槻塗装工業のホームページから"
            "送信したものを自動でお送りしています。\n"
            "お客様にご連絡する際は、お問い合わせ内容に記載してある"
            "メールアドレスまたは電話番号をご利用ください。\n"
            "=============================\n"
            "有限会社大槻塗装工業\n"
            "〒238-0032 神奈川県横須賀市平作2-20-2\n"
            "Tel 090-2564-5015\n"
            "email info@ohtsuki-tosou.ne.jp\n"
            "HP  https://www.ohtsuki-tosou.co.jp\n"
            "LP https://www.ohtsuki-tosou.com\n"
            "=============================\n"
        )

        #to smart
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(settings.MYMAIL, settings.MYMAILPASS)
        msg = MIMEText(email_msg)

        msg['Subject'] ="無料相談のお問い合わせ"
        msg['From'] = settings.MYMAIL
        msg['To'] = settings.SMARTMAIL
        msg['Date'] = formatdate()
        smtpobj.sendmail(settings.MYMAIL, settings.SMARTMAIL, msg.as_string())
        smtpobj.close()

        email_msg=(
            "お客様より無料相談のお問い合わせがありました。\n"
            "スマートリノベーションが担当しているフォームなので、\n"
            "対応不要です。これは確認のメールです。"
            "=============================\n"
            "▽お問い合わせ内容\n"
            "=============================\n"
            "\n【おなまえ】\n"
            +str(hurigana)+
            "\n【お名前】\n"
            +str(name)+
            "\n【ご年齢】\n"
            +str(old)+'歳'
            "\n【郵便番号】\n"
            +str(yubin)+
            "\n【ご住所】\n"
            +str(stay)+
            "\n【メールアドレス】\n"
            +str(email)+
            "\n【お電話番号】\n"
            +str(tel)+
            "\n【連絡希望日時】\n"
            "<第一希望>\n"
            +str(o_d.year)+'年'+str(o_d.month)+'月'+str(o_d.day)+'日'+str(one)+
            "\n<第二希望>\n"
            +str(t_d.year)+'年'+str(t_d.month)+'月'+str(t_d.day)+'日'+str(two)+
            "\n【現行金利】\n"
            +str(k_more)+
            "\n【残債額】\n"
            +str(s_more)+
            "\n【残年数】\n"
            +str(n_more)+
            "\n【年収】\n"
            +str(nensyu)+
            "\n【紹介コード】\n"
            + str(afi)+
            "\n=============================\n"
            "\n"
            "このメールはお客様が大槻塗装工業のホームページから"
            "送信したものを自動でお送りしています。\n"
            "お客様にご連絡する際は、お問い合わせ内容に記載してある"
            "メールアドレスまたは電話番号をご利用ください。\n"
            "=============================\n"
            "\n"
            "有限会社大槻塗装工業\n"
            "〒238-0032 神奈川県横須賀市平作2-20-2\n"
            "Tel 090-2564-5015\n"
            "email info@ohtsuki-tosou.ne.jp\n"
            "HP  https://www.ohtsuki-tosou.co.jp\n"
            "LP https://www.ohtsuki-tosou.com\n"
            "=============================\n"
        )

        #to ohtsuki
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(settings.MYMAIL, settings.MYMAILPASS)
        msg = MIMEText(email_msg)

        msg['Subject'] ="無料相談のお問い合わせ"
        msg['From'] = settings.MYMAIL
        msg['To'] = settings.OHTSUKIMAIL
        msg['Date'] = formatdate()
        smtpobj.sendmail(settings.MYMAIL, settings.OHTSUKIMAIL, msg.as_string())
        smtpobj.close()

        #to technext
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(settings.MYMAIL, settings.MYMAILPASS)
        msg = MIMEText(email_msg)

        msg['Subject'] ="無料相談のお問い合わせ"
        msg['From'] = settings.MYMAIL
        msg['To'] = settings.TECHBEEMAIL
        msg['Date'] = formatdate()
        smtpobj.sendmail(settings.MYMAIL, settings.TECHBEEMAIL, msg.as_string())
        smtpobj.close()


        return redirect('complete')
    return redirect('easy')

def complete_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/account.html')

def good_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/account.html',params)

def present_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/gai.html',params)

def mitumori_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/mitumori.html',params)

def e_s_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/nai.html',params)

def page_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/page.html',params)

def renovation_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/renovation.html',params)

def line_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/ful_contact.html',params)

def qa_view(request):
    qa_list=qa_model.objects.all()
    params={
        'aaa':qa_list,
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/qa.html',params)

def catalog_view(request):
    catalog=catalog_model.objects.all()
    params={
        'ccc':catalog,
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/catalog.html',params)

#見積依頼
def m_form_view(request):
    if request.method=='POST':
        afi=request.POST['afi']
        hurigana=request.POST['hurigana']
        name=request.POST['name']
        yubin=request.POST['yubin']
        stay=request.POST['stay']
        email=request.POST['email']
        tel=request.POST['tel']
        question_area=request.POST['question_area']
        one_day=request.POST['one_day']
        o_d = datetime.datetime.strptime(one_day, '%Y-%m-%d')
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
        t_d = datetime.datetime.strptime(two_day, '%Y-%m-%d')
        two=request.POST['two']
        if two == '1':
            two='9:00-12:00'
        elif two =='2':
            two='12:00-15:00'
        elif two == '3':
            two='15:00-18:00'
        else:
            two='18:00-20:00'

        #to customer
        email_msg=(
            "お問い合わせの送信が完了しました。\n"
            "担当の者からの連絡をお待ちください。\n"
            "=============================\n"
            "▽お問い合わせ内容\n"
            "=============================\n"
            "【おなまえ】\n"
            +str(hurigana)+
            "\n【お名前】\n"
            +str(name)+
            "\n【郵便番号】\n"
            +str(yubin)+
            "\n【ご住所】\n"
            +str(stay)+
            "\n【メールアドレス】\n"
            +str(email)+
            "\n【お電話番号】\n"
            +str(tel)+
            "\n【連絡希望日時】\n"
            "<第一希望>\n"
            +str(o_d.year)+'年'+str(o_d.month)+'月'+str(o_d.day)+'日'+str(one)+
            "\n<第二希望>\n"
            +str(t_d.year)+'年'+str(t_d.month)+'月'+str(t_d.day)+'日'+str(two)+
            "\n【ご質問等】\n"
            +str(question_area)+
            "\n【紹介コード】\n"
            +str(afi)+
            "\n===========================\n"
            "このメールはお客様が大槻塗装工業のホームページから"
            "送信したものを自動でお送りしています。\n"
            "その他追加でお問い合わせがございましたら、"
            "本メールに返信することも可能です。\n"
            "希望の連絡日時に沿えなかった際は、"
            "メールにて再度連絡希望日時をご確認させていただくことをご了承ください。\n"
            "=============================\n"
            "有限会社大槻塗装工業\n"
            "〒238-0032 神奈川県横須賀市平作2-20-2\n"
            "Tel 090-2564-5015\n"
            "email info@ohtsuki-tosou.ne.jp\n"
            "HP  https://www.ohtsuki-tosou.co.jp/\n"
            "LP https://www.ohtsuki-tosou.com/\n"
            "=============================\n"
        )

        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(settings.MYMAIL, settings.MYMAILPASS)
        msg = MIMEText(email_msg)

        msg['Subject'] = '大槻塗装見積依頼'
        msg['From'] = settings.MYMAIL
        msg['To'] = email
        msg['Date'] = formatdate()
        smtpobj.sendmail(settings.MYMAIL, email, msg.as_string())
        smtpobj.close()


        #to staff
        email_msg=(
            "お客様からお問い合わせがありました。\n"
            "=============================\n"
            "▽お問い合わせ内容\n"
            "=============================\n"
            "【おなまえ】\n"
            +str(hurigana)+
            "\n【お名前】\n"
            +str(name)+
            "\n【郵便番号】\n"
            +str(yubin)+
            "\n【ご住所】\n"
            +str(stay)+
            "\n【メールアドレス】\n"
            +str(email)+
            "\n【お電話番号】\n"
            +str(tel)+
            "\n【連絡希望日時】\n"
            "<第一希望>\n"
            +str(o_d.year)+'年'+str(o_d.month)+'月'+str(o_d.day)+'日'+str(one)+
            "\n<第二希望>\n"
            +str(t_d.year)+'年'+str(t_d.month)+'月'+str(t_d.day)+'日'+str(two)+
            "\n【ご質問等】\n"
            +str(question_area)+
            "\n【紹介コード】\n"
            +str(afi)+
            "\n=========================\n"
            "このメールはお客様が大槻塗装工業のホームページから"
            "送信したものを自動でお送りしています。\n"
            "お客様にご連絡する際は、お問い合わせ内容に記載してある"
            "メールアドレスまたは電話番号をご利用ください。\n"
            "=============================\n"
            "有限会社大槻塗装工業\n"
            "〒238-0032 神奈川県横須賀市平作2-20-2\n"
            "Tel 090-2564-5015\n"
            "email info@ohtsuki-tosou.ne.jp\n"
            "HP  https://www.ohtsuki-tosou.co.jp/\n"
            "LP https://www.ohtsuki-tosou.com/\n"
            "=============================\n"
        )
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(settings.MYMAIL, settings.MYMAILPASS)
        msg = MIMEText(email_msg)

        msg['Subject'] = str(name)+'さんから見積依頼'
        msg['From'] = settings.MYMAIL
        msg['To'] = settings.OHTSUKIMAIL
        msg['Date'] = formatdate()
        smtpobj.sendmail(settings.MYMAIL,settings.OHTSUKIMAIL , msg.as_string())
        smtpobj.close()

        msg['Subject'] = str(name)+'さんから見積依頼'
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(settings.MYMAIL, settings.MYMAILPASS)
        msg = MIMEText(email_msg)

        msg['From'] = settings.MYMAIL
        msg['To'] = settings.TECHBEEMAIL
        msg['Date'] = formatdate()
        smtpobj.sendmail(settings.MYMAIL,settings.TECHBEEMAIL , msg.as_string())
        smtpobj.close()

        return redirect('good')
    return redirect('index')

def regi_view(request):
    params={
        'afi_code':'',
    }
    try:
        social_account=SocialAccount.objects.get(user=request.user)
        meta=user_meta.objects.get(uid=social_account.uid)
    except:
        params['afi_code']='000000'
    else:
        params['afi_code']=meta.afi_code
    return render(request,'tosou/regi.html',params)

@login_required
def account_view(request):
    user=request.user
    params={
        'afi_code':'000000',
        'line_regi':False,
    }
    if settings.DEBUG==False:
        if request.user.is_authenticated:
            try:
                social_account=SocialAccount.objects.get(user=request.user)
            except:
                pass
            else:
                try:
                    meta=user_meta.objects.get(uid=social_account.uid)
                except:
                    headers = {
                        'Authorization': 'Bearer '+settings.YOUR_CHANNEL_ACCESS_TOKEN,
                    }
                    request_url='https://api.line.me/v2/bot/profile/'+str(social_account.uid)
                    r = requests.get(request_url, headers=headers)
                    data = json.loads(r.text)
                    name=data["displayName"]
                    top=data['pictureUrl']
                    code=code_model.objects.get(option=0)
                    afi_code='{:0=6}'.format(int(code.num))
                    code.num+=1
                    code.save()
                    meta=user_meta(username=str(name),top=str(top),afi_code=str(afi_code),uid=str(social_account.uid))
                    meta.save()


                params['afi_code']=meta.afi_code
                params['line_regi']=True


    return render(request,'tosou/account.html',params)
