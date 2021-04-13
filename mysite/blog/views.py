from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.views.generic import ListView
from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


'''
def post_list(request):
    object_list = Post.published.all()
    # Display three posts on each page:
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # When the page is not an integer, simple deliver the first page:
        posts = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, then display the last page of results:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})
'''


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    # Retrieve our post by id:
    post = get_object_or_404(Post, id=post_id, status='published')
    # Used to handle success message in our template:
    sent = False

    # POST our form data
    if (request.method == 'POST'):
        # Form was submitted:
        form = EmailPostForm(request.POST)

        # [CASE] Form is successfully validated:
        if form.is_valid():
            # Send email sharing post title + post URL:
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends that you read {post.title}"
            message = f"You can read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'copev313@gmail.com', [cd['to']])
            sent = True

        # [CASE] Form didn't pass validation:
        else:
            form = EmailPostForm()

        return render(request,
                      'blog/post/share.html',
                      {'post': post,
                       'form': form,
                       'sent': sent})
