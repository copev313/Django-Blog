from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer then deliver the first page:
        posts = paginator.page(1)

    except EmptyPage:
        # If page is out of range then deliver last page of results:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts, 'page': page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,  slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)

    # List of active comments for this post:
    comments = post.comments.filter(active=True)

    new_comment = None

    # [CASE] POST a new comment:
    if (request.method == 'POST'):
        # A comment was posted:
        comment_form = CommentForm(data=request.POST)
        # Comment form is valid:
        if comment_form.is_valid():
            # Create Comment object:
            new_comment = comment_form.save(commit=False)
            # Assign the current blog post to the comment:
            new_comment.post = post
            # Save the comment to the database:
            new_comment.save()
    
    # [CASE] GET request:
    else:
        comment_form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  { 'post': post,
                    'comments': comments,
                    'new_comment': new_comment,
                    'comment_form': comment_form})


def post_share(request, post_id):
    # Retrieve our post by id:
    post = get_object_or_404(Post, id=post_id, status='published')
    # Used to handle success message in our template:
    sent = False

    # [CASE] POST our form data:
    if (request.method == 'POST'):
        # Form was submitted:
        form = EmailPostForm(request.POST)

        # [CASE] Form is successfully validated:
        if form.is_valid():
            # Send email sharing post title + post URL:
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends that you read \"{post.title}\""
            message = f"You can read \"{post.title}\" at:  {post_url}\n\n" \
                      f"{cd['name']}'s comments:\n\n\t{cd['comments']}" \
                      "\n\nSincerely,\n📨 EMAILBOT @ MyDjangoBlog.com 🤖"
            send_mail(subject, message, 'copev313@gmail.com', [cd['to']])
            sent = True

    # [CASE] GET our form:
    else:
        form = EmailPostForm()

    return render(request,
                  'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})
