from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from accounts.models import Profile
from bookmark.models import Bookmark


class BookmarkListView(ListView):
    model = Bookmark

    # bookmark_list.html, {'bookmark_list': Bookmark.objects.all()}

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:  # 로그인 하면, 로그인한 사용자의 북마크만 보이자
            # user -> profile -> bookmark_list
            profile = Profile.objects.get(user=user)  # user -> profile
            bookmark_list = Bookmark.objects.filter(profile=profile)  # profile -> bookmark_list
        else:  # 로그인 안하면,
            # bookmark_list = Bookmark.objects.all()    #북마크 다 보여주자
            bookmark_list = Bookmark.objects.none()  # 북마크 보이지 말자
        return bookmark_list


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['profile', 'name', 'url']  # '__all__'
    template_name_suffix = '_create'  # bookmark_form.html -> bookmark_create.html
    success_url = reverse_lazy('bookmark:list')

    def get_initial(self):
        # user -> profile
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return {'profile': profile}


class BookmarkDetailView(LoginRequiredMixin, DetailView):
    model = Bookmark


class BookmarkUpdateView(LoginRequiredMixin, UpdateView):
    model = Bookmark
    fields = ['name', 'url']  # '__all__'
    template_name_suffix = '_update'  # bookmark_update.html
    # success_url = reverse_lazy('bookmark:list')   #success_url 없으면 model의 get_absolute_url() 호출


class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:list')


def list_bookmark(request):
    # 로그인 사용자 확인하자
    user = request.user
    if user.is_authenticated:    # 로그인 되어있으면
        profile = Profile.objects.get(user=user)
        bookmark_list = Bookmark.objects.filter(profile=profile)  # 그 사용자의 북마크 가져오자
    else:   # 로그인 안되어 있으면
        bookmark_list = Bookmark.objects.none()    # 북마크 없는것 가져오자

    return render(request, 'bookmark/bookmark_list.html', {'bookmark_list': bookmark_list})


def detail_bookmark(request, pk):
    bookmark = Bookmark.objects.get(pk=pk)
    return render(request, 'bookmark/bookmark_detail.html', {'bookmark': bookmark})