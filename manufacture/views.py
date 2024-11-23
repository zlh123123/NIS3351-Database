from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .login_form import LoginForm, RegisterForm
from django.contrib import messages
from manufacture.function import *
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request: HttpRequest):
    return render(request, "home/home.html")


def log(request: HttpRequest):
    if request.session.get("is_login", None):
        return redirect("/dashboard/")

    if request.method == "GET":
        return render(request, "home/login.html")

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data["log_username"]
            password = login_form.cleaned_data["log_password"]

            login_result = login(username, password)

            if login_result == 0:
                request.session["is_login"] = True
                request.session["user_name"] = username
                return redirect("/dashboard/")
            elif login_result == 1:
                messages.error(request, "密码错误！")
            elif login_result == -1:
                messages.error(request, "用户不存在！")

            return render(request, "home/login.html", locals())

        elif register_form.is_valid():
            username = register_form.cleaned_data["reg_username"]
            # email = register_form.cleaned_data["reg_email"]
            password = register_form.cleaned_data["reg_password"]
            password2 = register_form.cleaned_data["reg_password2"]

            reg_result = register(username, password)

            if reg_result == 0:
                messages.success(request, "注册成功！")
                return redirect("/login/")
            elif reg_result == 1:
                messages.error(request, "用户已存在！")

            return render(request, "home/login.html", locals())


def logout(request: HttpRequest):
    if not request.session.get("is_login", None):
        return redirect("/home/")
    request.session.flush()
    return redirect("/home/")


def mainpage(request):
    if not request.session.get("is_login", None):
        return render(request, "mainpage/mainpage.html")
    user_info = check_user(request.session.get("user_name", None))
    context = {
        "login_result": request.session.get("is_login", None),
        "image_url": user_info.image,
        "user_id": user_info.id,
    }
    return render(request, "mainpage/mainpage.html", context)


def search(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    search_word = request.GET.get("search_word")
    notice_list = search_notice_content(search_word)
    if notice_list:
        notice_count = len(notice_list)
    else:
        notice_count = 0
    context = {
        "login_result": request.session.get("is_login", None),
        "search_word": search_word,
        "notice_count": notice_count,
    }

    if not search_word:
        return redirect("/dashboard/")
    return render(request, "mainpage/waterfallshowcard/search.html", context)


def get_search_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    search_word = request.GET.get("search_word")
    notice_list = search_notice_content(search_word)
    if not notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [serialize_notice(notice) for notice in notice_list]

    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def dashboard_recommend(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "mainpage/waterfallshowcard/recommend.html")


def get_recommend_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    notice_list = check_all_notice()

    if not notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [serialize_notice(notice) for notice in notice_list]
    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def dashboard_sports(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "mainpage/waterfallshowcard/sports.html")


def get_sports_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    sport_notice_list = search_notice_type(1)

    if not sport_notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [
            serialize_notice(notice) for notice in sport_notice_list
        ]

    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def dashboard_emotion(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "mainpage/waterfallshowcard/emotion.html")


def get_emotion_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    emotion_notice_list = search_notice_type(6)

    if not emotion_notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [
            serialize_notice(notice) for notice in emotion_notice_list
        ]

    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def dashboard_food(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "mainpage/waterfallshowcard/food.html")


def get_food_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    food_notice_list = search_notice_type(3)

    if not food_notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [
            serialize_notice(notice) for notice in food_notice_list
        ]

    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def dashboard_study(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "mainpage/waterfallshowcard/study.html")


def get_study_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    study_notice_list = search_notice_type(2)

    if not study_notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [
            serialize_notice(notice) for notice in study_notice_list
        ]

    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def dashboard_travel(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "mainpage/waterfallshowcard/travel.html")


def get_travel_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    travel_notice_list = search_notice_type(5)

    if not travel_notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [
            serialize_notice(notice) for notice in travel_notice_list
        ]

    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def dashboard_games(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "mainpage/waterfallshowcard/games.html")


def get_games_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    game_notice_list = search_notice_type(4)

    if not game_notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [
            serialize_notice(notice) for notice in game_notice_list
        ]

    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def main(request, post_id):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    post = check_notice(post_id)
    author = check_notice_owner(post.id)
    # 还需要当前用户的信息，通过用户名获取用户类
    if author.user_name == request.session.get("user_name", None):
        is_myself = True
    else:
        is_myself = False

    if post.if_disabled:
        if is_myself:
            is_disabled = True
        else:
            messages.error(request, "该通知已被挂起！")
            return redirect("/dashboard/")
    else:
        is_disabled = False

    apply_result = check_request_state(
        post_id, name_to_id(request.session.get("user_name", None))
    )

    if apply_result == 1:
        owner_contact = post.owner_contact
    else:
        owner_contact = "unknown"

    context = {
        "post": post,
        "author": author,
        "is_myself": is_myself,
        "is_disabled": is_disabled,
        "apply_result": apply_result,
        "owner_contact": owner_contact,
    }
    return render(request, "mainpage/main.html", context)


def applylist(request, post_id):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    user_list = check_request_user(post_id)
    user_info_list = []
    if user_list:
        for user_id in user_list:
            user = check_user(id_to_name(user_id))
            request_state = check_request_state(post_id, user_id)
            user_info_list.append((user, request_state, post_id))

    return render(request, "mainpage/applylist.html", {"user_list": user_info_list})


def handle_answer_request(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        post_id = request.POST.get("post_id")
        action = request.POST.get("action")  # {1：同意，2：拒绝}

        # 调用 answer_request 函数
        user_name = user_id_to_name(user_id)
        result = answer_request(post_id, user_name, action)

        return JsonResponse({"success": True, "result": result})

    return JsonResponse({"success": False, "message": "请求失败"}, status=400)


def yinsixieyi(request):
    return render(request, "mainpage/yinsixieyi.html")


def kefu(request):
    return render(request, "mainpage/kefu.html")


def my(request, user_id):
    if request.method == "GET":
        if request.session.get("is_login", None):
            username = id_to_name(user_id)
            user_info = check_user(username)
            if user_info.introduction == "unknown":
                user_info.introduction = "这个人还没有个人介绍"

            my_username = request.session["user_name"]
            if username == my_username:
                is_myself = True
            else:
                is_myself = False
            context = {
                "user_nickname": user_info.nickname,
                "user_introduction": user_info.introduction,
                "user_avatar": user_info.image,
                "user_id": user_info.id,
                "is_myself": is_myself,
            }
            return render(request, "user/my.html", context)
        else:
            messages.error(request, "请先登录！")
            return redirect("/login/")


def change_username(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    if request.method == "POST":
        new_nickname = request.POST.get("username")
        username = request.session["user_name"]
        user_id = name_to_id(username)

        user_info = check_user(username)
        old_nickname = user_info.nickname

        if new_nickname == old_nickname:
            messages.error(request, "新昵称不能与旧昵称相同！")
            return redirect(f"/my/{user_id}/")

        if len(new_nickname) > 10:
            messages.error(request, "昵称长度不能超过10个字符！")
            return redirect(f"/my/{user_id}/")

        user_info.nickname = new_nickname
        result = change_user_info(user_info)
        if result == 0:
            messages.success(request, "修改成功！")
            return redirect(f"/my/{user_id}/")
        else:
            messages.error(request, "修改失败！")
            return redirect(f"/my/{user_id}/")

    return render(request, "user/myoptions/mychangeinfo.html")


def change_desc(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    if request.method == "POST":
        new_desc = request.POST.get("desc")
        username = request.session["user_name"]
        user_id = name_to_id(username)

        if new_desc == "":
            messages.error(request, "个人介绍不能为空！")
            return redirect(f"/my/{user_id}")

        user_info = check_user(username)
        user_info.introduction = new_desc
        result = change_user_info(user_info)

        if result == 0:
            messages.success(request, "修改成功！")
            return redirect(f"/my/{user_id}")
        else:
            messages.error(request, "修改失败！")
            return redirect(f"/my/{user_id}")

    return render(request, "user/myoptions/mychangeinfo.html")


def change__password(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        username = request.session["user_name"]
        user_id = name_to_id(username)

        if not re.match(r"^[a-zA-Z0-9]{6,18}$", new_password):
            messages.error(request, "密码必须为6-18位字母或数字！")
            return redirect(f"/my/{user_id}")

        if old_password == new_password:
            messages.error(request, "新密码不能与旧密码相同！")
            return redirect(f"/my/{user_id}")

        result = change_password(username, old_password, new_password)

        if result == 0:
            messages.success(request, "修改成功！")
            return redirect(f"/my/{user_id}")
        elif result == 1:
            messages.error(request, "旧密码错误！")
            return redirect(f"/my/{user_id}")

    return render(request, "user/myoptions/mychangeinfo.html")


def change_avatar(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    if request.method == "POST":
        image_url = request.POST.get("image_url")
        username = request.session["user_name"]
        user_id = name_to_id(username)

        if image_url == "":
            messages.error(request, "请先上传图片！")
            return redirect(f"/my/{user_id}")

        user_info = check_user(username)
        user_info.image = image_url
        result = change_user_info(user_info)

        if result == 0:
            messages.success(request, "修改成功！")
            return redirect(f"/my/{user_id}")
        else:
            messages.error(request, "修改失败！")
            return redirect(f"/my/{user_id}")

    return render(request, "user/myoptions/mychangeinfo.html")


def published(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "user/myoptions/mypublished.html")


def get_my_published_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    notice_list = check_my_notice(request.session.get("user_name", None))
    if not notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [serialize_notice(notice) for notice in notice_list]
    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


@csrf_exempt
def publish(request):
    if not request.session.get("is_login", None):
        return redirect("/login/")  # 如果未登录，重定向到仪表盘

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            title = data.get("title", "unknown")  # 默认值为"unknown"
            contact = data.get("contact")
            content = data.get("content")
            category = data.get("category", 0)  # 默认值为0
            tags = data.get("tags") if data.get("tags") else []  # 确保 tags 是一个列表
            # 测试tags
            # print(tags)
            image_url = data.get("imageUrl")
            current_date = data.get("date", "unknown")  # 默认值为"unknown"
            notice_id = add_notice(
                request.session["user_name"]
            )  # 传入当前用户名或用户ID
            # print(notice_id)
            if notice_id == -1:
                return JsonResponse({"error": "用户不存在"}, status=400)

            notice = check_notice(notice_id)
            if notice is None:
                return JsonResponse({"error": "获取通知失败"}, status=400)

            notice.owner_contact = contact
            notice.title = title
            notice.basic_type = category
            notice.image = image_url
            notice.time = current_date
            notice.description = content
            # 将tags转化为字符串，两项之间用空格隔开
            # tags = ' '.join(tags)
            # print(tags)

            notice.tag = tags
            # print(notice.tag)

            if change_notice(notice) == -1:
                return JsonResponse({"error": "更新通知失败"}, status=400)

            return JsonResponse({"message": "发布成功"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "发布失败，数据格式错误"}, status=400)

    return render(request, "user/push.html")


def replied(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "user/myoptions/myreplied.html")


def get_my_replied_notice(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    notice_list = check_request_notice(request.session.get("user_name", None))
    if not notice_list:
        serialize_notice_list = []
    else:
        serialize_notice_list = [serialize_notice(notice) for notice in notice_list]
    return JsonResponse({"notice_list": serialize_notice_list}, safe=False)


def info(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "user/myoptions/mychangeinfo.html")


def message(request):
    if not request.session.get("is_login", None):
        messages.error(request, "请先登录！")
        return redirect("/login/")
    return render(request, "user/message.html")


@csrf_exempt
def disable__notice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            notice_id = data.get("notice_id")
            post = check_notice(notice_id)
            if not request.session.get("user_name", None):
                return JsonResponse(
                    {"success": -1, "message": "未登录", "error": str(e)}
                )

            elif id_to_name(post.owner_id) != request.session.get("user_name", None):
                return JsonResponse(
                    {"success": -2, "message": "无权限删除", "error": str(e)}
                )

            result = disable_notice(notice_id)
            print(result)

            if result == 0:
                return JsonResponse({"success": 0, "message": "删除成功"})
            else:
                return JsonResponse({"success": -3, "message": "删除失败"})

        except Exception as e:
            return JsonResponse({"success": -3, "message": "删除失败", "error": str(e)})


@csrf_exempt
def recover_notice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            notice_id = data.get("notice_id")
            post = check_notice(notice_id)
            if not request.session.get("user_name", None):
                return JsonResponse(
                    {"success": -1, "message": "未登录", "error": str(e)}
                )

            elif id_to_name(post.owner_id) != request.session.get("user_name", None):
                return JsonResponse(
                    {"success": -2, "message": "无权限恢复", "error": str(e)}
                )

            result = enable_notice(notice_id)
            print(result)

            if result == 0:
                return JsonResponse({"success": 0, "message": "恢复成功"})
            else:
                return JsonResponse({"success": -3, "message": "恢复失败"})

        except Exception as e:
            return JsonResponse({"success": -3, "message": "恢复失败", "error": str(e)})


@csrf_exempt
def request_notice_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            notice_id = data.get("notice_id")
            # user_name = data.get("user_name")
            print(notice_id)
            print(request.session["user_name"])
            notice = check_notice(notice_id)

            if request.session["user_name"] == id_to_name(notice.owner_id):
                return JsonResponse(
                    {"success": -5, "error": "不能请求自己发布的通知"}, status=400
                )

            result = request_notice(notice_id, request.session["user_name"])
            return JsonResponse({"success": result})
        except json.JSONDecodeError:
            return JsonResponse({"success": -3, "error": "数据格式错误"}, status=400)
    return JsonResponse({"success": -4, "error": "无效的请求方法"}, status=405)
