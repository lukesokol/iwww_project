from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Category, Photo, UserProfile
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from photos.forms import UserProfileForm

def board(request):
    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.all().order_by('-views')
    else:
        photos = Photo.objects.filter(category__name=category).order_by('-views')

    context_dict = {}
    context_dict['photos'] = photos

    return render(request, 'photos/board.html', context_dict)

@login_required
def add_photo(request):
    current_user = request.user
    categories = Category.objects.all()

    context_dict = {}
    context_dict['categories'] = categories

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
            author=current_user,
        )

        return redirect('board')

    return render(request, 'photos/add_photo.html', context_dict)

def view_photo(request, pk):
    try:
        photo = Photo.objects.get(id=pk)
    except Photo.DoesNotExist:
        return redirect(reverse('board'))

    photo.views = photo.views + 1
    photo.save()

    context_dict = {'photo': photo}
    return render(request, 'photos/view_photo.html', context_dict)

def like_photo(request):
    photo_id = request.GET.get('photo_id')

    try:
        photo = Photo.objects.get(id=int(photo_id))
    except Photo.DoesNotExist:
        return HttpResponse(-1)
    except ValueError:
        return HttpResponse(-1)

    photo.likes = photo.likes + 1
    photo.save()

    return HttpResponse(photo.likes)

class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'photos/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('board'))
        else:
            print(form.errors)

        context_dict = {'form': form}
        return render(request, 'photos/profile_registration.html', context_dict)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website, 'picture': user_profile.picture})

        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('board'))

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}

        return render(request, 'photos/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('board'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('profile', kwargs={'username': username}))
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}

        return render(request, 'photos/profile.html', context_dict)

class CategorySuggestionView(View):
    def get(self, request):
        suggestion = request.GET['suggestion']
        category_list = get_category_list(max_results=8, starts_with=suggestion)

        if len(category_list) == 0:
            category_list = Category.objects.all()

        return render(request, 'photos/categories.html', {'categories': category_list})

def get_category_list(max_results=0, starts_with=''):
    category_list = []

    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]

    return category_list