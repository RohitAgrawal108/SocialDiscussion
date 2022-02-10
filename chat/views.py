from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from chat.models import Thread, Message
from django.contrib.auth.models import User
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:123zxcvbnm@localhost:5432/SocialDiscussion')

logedd_in_user_id = 1

print("In CHAT VIEWS")

def template_view(request):
    context = {}
    context['me'] = request.user
    chat_thread_users_sidebar=pd.read_sql_query('select * from "chat_thread_users"',con=engine)
    # chat_thread_sidebar=pd.read_sql_query('select * from "chat_thread"',con=engine)
    auth_user_sidebar=pd.read_sql_query('select * from "auth_user"',con=engine)
    users_treads_sidebar = chat_thread_users_sidebar[chat_thread_users_sidebar.user_id == request.user.id].thread_id

    user_id_list = list()
    for i in list(users_treads_sidebar):
        user_id_list = user_id_list + list(chat_thread_users_sidebar[chat_thread_users_sidebar.thread_id == i].user_id)
    user_id_list = list(set(user_id_list))
    user_id_list.remove(request.user.id)
    sidebar_list = list()
    for i in list(user_id_list):
        
        if i != request.user.id:
            name = auth_user_sidebar[auth_user_sidebar.id==i].values.tolist()[0][4]
            sidebar_list.append(name)

    context['sidebar_list'] = sidebar_list
    return render(request, 'chat/ChatTemplate.html',context = context)


class ThreadView(View):
    chat_thread_users=pd.read_sql_query('select * from "chat_thread_users"',con=engine)
    chat_thread=pd.read_sql_query('select * from "chat_thread"',con=engine)
    auth_user=pd.read_sql_query('select * from "auth_user"',con=engine)
    
    def getuser_id(self):
        logedd_in_user_id = self.request.user
        return logedd_in_user_id

    template_name = 'chat/chat.html'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        self.other_user = get_user_model().objects.get(username=other_username)
        obj = Thread.objects.get_or_create_personal_thread(self.request.user, self.other_user)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context['me'] = self.request.user
        context['thread'] = self.get_object()
        context['user'] = self.other_user
        context['messages'] = self.get_object().message_set.all()
        chat_thread_users_sidebar=pd.read_sql_query('select * from "chat_thread_users"',con=engine)
        # chat_thread_sidebar=pd.read_sql_query('select * from "chat_thread"',con=engine)
        auth_user_sidebar=pd.read_sql_query('select * from "auth_user"',con=engine)
        users_treads_sidebar = chat_thread_users_sidebar[chat_thread_users_sidebar.user_id == self.request.user.id].thread_id

        user_id_list = list()
        for i in list(users_treads_sidebar):
            user_id_list = user_id_list + list(chat_thread_users_sidebar[chat_thread_users_sidebar.thread_id == i].user_id)
        user_id_list = list(set(user_id_list))
        user_id_list.remove(self.request.user.id)
        sidebar_list = list()
        for i in list(user_id_list):
            if i != self.request.user.id:
                name = auth_user_sidebar[auth_user_sidebar.id==i].values.tolist()[0][4]
                sidebar_list.append(name)
        context['sidebar_list'] = sidebar_list
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        logedd_in_user_id = self.request.user
        
        print(logedd_in_user_id)
        return render(request, 'chat/chat.html', context=context)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        thread = self.get_object()
        data = request.POST
        user = request.user
        text = data.get("message")
        Message.objects.create(sender=user, thread=thread, text=text)
        context = self.get_context_data(**kwargs)
        return render(request, 'chat/chat.html', context=context)

